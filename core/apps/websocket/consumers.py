import json
import logging

from channels.generic.websocket import AsyncWebsocketConsumer

from core.apps.websocket.models.notification import Notification

logger = logging.getLogger(__name__)


class NotificationConsumer(AsyncWebsocketConsumer):
    async def acknowledge_notification(self, notification_id: int):
        logger.debug(
            f"Attempting to acknowledge notification {notification_id} for user {self.user.id}"
        )
        try:
            notification = Notification.objects.get(
                id=notification_id, user=self.user
            )
            logger.debug(
                f"Notification {notification_id} found for user {self.user.id}"
            )
            notification.is_sending = True
            notification.is_read = True
            notification.save()
            logger.info(
                f"Notification {notification_id} acknowledged by user {self.user.id}"
            )
            logger.debug(
                f"Notification {notification_id} status: is_sending={notification.is_sending}, is_read={notification.is_read}"
            )
        except Notification.DoesNotExist:
            logger.warning(
                f"Notification {notification_id} does not exist for user {self.user.id}"
            )
        except Exception as e:
            logger.error(
                f"An error occurred while acknowledging notification {notification_id} for user {self.user.id}: {e}"
            )

    async def connect(self):
        self.user = self.scope["user"]
        if self.user.is_anonymous:
            await self.close()
        else:
            await self.channel_layer.group_add(
                f"user_{self.user.id}", self.channel_name
            )
            await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            f"user_{self.user.id}", self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        if data.get("type") == "acknowledge_notification":
            await self.acknowledge_notification(int(data["notification_id"]))
            print(
                f"Notification acknowledged {data['notification_id']} {self.user.id} {self.channel_name} {self.channel_layer}"
            )
            print(data)
        #     channel_layer = get_channel_layer()
        #     async_to_sync(channel_layer.group_send)(
        #         f"user_{self.user.id}",
        #         {
        #             "type": "acknowledge_notification",
        #             "notification_id": int(data["notification_id"]),
        #         }
        #     )
        #     notification = Notification.objects.get(id=int(data["notification_id"]), user=self.user)
        #     notification.refresh_from_db()
        #     notification.is_sending = True
        #     notification.save()
        # else:
        #     logger.warning(f"Unknown message type: {data.get('type')}")
        #     print(f"Unknown message type: {data.get('type')}")

    async def send_notification(self, event):
        message = event["message"]
        await self.send(text_data=message)
