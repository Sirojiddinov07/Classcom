from django.db.models.signals import post_save
from django.dispatch import receiver

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
