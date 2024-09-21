from celery import shared_task
from django.db import transaction

from core.apps.websocket.models import Notification


@shared_task
def create_notification_task(user_id, message_uz, message_ru):
    try:
        with transaction.atomic():
            Notification.objects.create(
                user_id=user_id, message_uz=message_uz, message_ru=message_ru
            )
            return {"status": "success", "user_id": user_id}
    except Exception as e:
        return {"status": "error", "user_id": user_id, "error": str(e)}
