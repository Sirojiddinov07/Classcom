import json
import logging

from asgiref.sync import sync_to_async, async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from django.db.models.signals import post_save
from django.dispatch import receiver

from core.apps.websocket.models.notification import Notification


class NotificationConsumer(AsyncWebsocketConsumer):
    async def acknowledge_notification(self, notification_id: int):
        logging.debug(
            f"Attempting to acknowledge notification {notification_id} for user {self.user.id}"
        )
        notification = await Notification.objects.aget(
            id=notification_id, user=self.user
        )
        logging.debug(
            f"Notification {notification_id} found for user {self.user.id}"
        )
        notification.is_read = True
        await notification.asave()

    async def connect(self):
        self.user = self.scope["user"]
        if self.user.is_anonymous:
            await self.close()
        else:
            await self.channel_layer.group_add(
                f"user_{self.user.id}", self.channel_name
            )
            await self.accept()

            notifications = await sync_to_async(list)(
                Notification.objects.filter(user=self.user, is_sending=False)
            )
            for notification in notifications:
                await self.send(
                    text_data=json.dumps(
                        {
                            "type": "send_notification",
                            "message": notification.message,
                            "notification_id": notification.id,
                        }
                    )
                )
                notification.is_sending = True
                await notification.asave()

            @receiver(post_save, sender=Notification)
            def notification_created(sender, instance, created, **kwargs):
                if created and instance.user == self.user:
                    async_to_sync(self.channel_layer.group_send)(
                        f"user_{self.user.id}",
                        {
                            "type": "send_notification",
                            "message": json.dumps(
                                {
                                    "type": "send_notification",
                                    "message": instance.message,
                                    "notification_id": instance.id,
                                }
                            ),
                        },
                    )
                    instance.is_sending = True
                    instance.save()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            f"user_{self.user.id}", self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        if data.get("type") == "acknowledge_notification":
            try:
                await self.acknowledge_notification(
                    int(data["notification_id"])
                )
            except Exception as e:
                print("=======")
                print(e)
                print("=======")
            print(
                f"Notification acknowledged {data['notification_id']} {self.user.id}"
                f" {self.channel_name} {self.channel_layer}"
            )
            print(data)

    async def send_notification(self, event):
        message = event["message"]
        await self.send(text_data=message)
