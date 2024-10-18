from django.db.models.signals import pre_save
from django.dispatch import receiver

from core.apps.accounts.tasks import send_congratulation_sms
from core.apps.classcom.choices import Role
from core.apps.classcom.models import Moderator


@receiver(pre_save, sender=Moderator)
def check_is_contracted_change(sender, instance, **kwargs):
    if instance.pk:
        old_instance = Moderator.objects.get(pk=instance.pk)
        if old_instance.is_contracted and not instance.is_contracted:
            print(
                f"Old: {old_instance.is_contracted} New: {instance.is_contracted}"
            )
            instance.user.role = Role.USER
            instance.user.save()
            print("Moderator role changed to user")
        elif not old_instance.is_contracted and instance.is_contracted:
            print(
                f"Old: {old_instance.is_contracted} New: {instance.is_contracted}"
            )
            first_name = instance.user.first_name
            last_name = instance.user.last_name
            phone = instance.user.phone
            instance.user.role = Role.MODERATOR
            instance.user.save()
            send_congratulation_sms.delay(phone, first_name, last_name)
            print("Moderator confirmed")
