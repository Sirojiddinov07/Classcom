from asgiref.sync import async_to_sync
from celery import shared_task
from celery.utils.log import get_task_logger
from channels.layers import get_channel_layer
from django.core.exceptions import ObjectDoesNotExist

from core.apps.websocket.models.notification import Notification

logger = get_task_logger(__name__)


@shared_task(bind=True, max_retries=None, default_retry_delay=5)
def send_notification_task(self, notification_id):
    try:
        notification = Notification.objects.get(id=notification_id)
        if not notification.is_sending:
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f"user_{notification.user.id}",
                {
                    "type": "send_notification",
                    "message": notification.message,
                    "notification_id": notification_id,
                },
            )
            logger.info(f"Notification sent to user {notification.user.id}")
        else:
            logger.info(
                f"Notification {notification_id} already acknowledged by user {notification.user.id}"
            )
    except ObjectDoesNotExist:
        logger.warning(
            f"Notification with id {notification_id} does not exist. Retrying..."
        )
        self.retry(
            exc=ObjectDoesNotExist(
                f"Notification with id {notification_id} does not exist"
            )
        )
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise e
    else:
        notification.refresh_from_db()
        if not notification.is_sending:
            self.retry(exc=Exception("Notification not acknowledged yet"))
