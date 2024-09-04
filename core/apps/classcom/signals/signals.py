from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from core.apps.websocket.models.notification import Notification
from ..models import TempModerator, Moderator, Topic
from ..models.feedback import Answer


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
            science_type=instance.science_type,
            degree=instance.degree,
            docs=instance.docs,
            is_contracted=instance.is_contracted,
        )
        instance.delete()


@receiver(post_delete, sender=Topic)
def reorder_topics_on_delete(sender, instance, **kwargs):
    plans = (
        instance.plan_set.all()
    )  # Retrieve all plans associated with the topic
    for plan in plans:
        related_topics = plan.topics.all().order_by("sequence_number")
        for index, topic in enumerate(related_topics, start=1):
            topic.sequence_number = index
            topic.save()
