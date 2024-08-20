from django.db.models.signals import post_save
from django.dispatch import receiver

from core.apps.accounts.tasks import send_congratulation_sms
from core.apps.classcom.models import Moderator


@receiver(post_save, sender=Moderator)
def moderator_confirmed_handler(sender, instance, **kwargs):
    if (
        instance.is_contracted
        and "is_contracted" in instance.get_dirty_fields()
    ):
        first_name = instance.user.first_name
        last_name = instance.user.last_name
        phone = instance.user.phone
        send_congratulation_sms.delay(phone, first_name, last_name)
        print("SMS sent")
