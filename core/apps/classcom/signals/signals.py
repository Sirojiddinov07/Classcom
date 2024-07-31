from django.db.models.signals import post_save
from django.dispatch import receiver

from ..models import TempModerator, Moderator
from ..models.feedback import Answer
from ..models.notification import Notification


@receiver(post_save, sender=Answer)
def notify_user_on_answer(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.feedback.user, message=instance.body
        )

        feedback = instance.feedback
        feedback.answered = True
        feedback.save()

@receiver(post_save, sender=TempModerator)
def create_moderator(sender, instance, created, **kwargs):
    if instance.is_contracted:
        Moderator.objects.create(
            user=instance.user,
            balance=instance.balance,
            science=instance.science,
            classes=instance.classes,
            degree=instance.degree,
            docs=instance.docs,
            is_contracted=instance.is_contracted
        )
        instance.delete()