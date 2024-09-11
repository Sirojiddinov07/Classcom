import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Orders
from .tasks import update_price_task

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Orders)
def order_create(sender, instance, created, **kwargs):
    """Order post save signal"""
    if not kwargs.get("skip_signal", False) and created:
        update_price_task.delay(instance.id)
        logger.info(f"Order {instance.id} created")
