from django.db.models.signals import post_save
from django.dispatch import receiver

from core.apps.websocket.models.notification import Notification
from core.apps.websocket.tasks.notification import send_notification_task


@receiver(post_save, sender=Notification)
def notification_created(sender, instance, created, **kwargs):
    if created:
        send_notification_task.delay(instance.id)
        print("Notification created")
