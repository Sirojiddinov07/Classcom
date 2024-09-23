from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from core.apps.websocket.models.notification import Notification
from ..models import Topic, Plan, Chat
from ..models.feedback import Answer


@receiver(post_save, sender=Answer)
def notify_user_on_answer(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.feedback.user, message_uz=instance.body
        )

        feedback = instance.feedback
        feedback.answered = True
        feedback.save()


@receiver(pre_delete, sender=Topic)
def reorder_topics_on_delete(sender, instance, **kwargs):
    plans = Plan.objects.filter(topic=instance).distinct()
    if not plans.exists():
        print(f"No Plans found for Topic: {instance}")
    else:
        for plan in plans:
            related_topics = (
                plan.topic.all()
                .order_by("sequence_number")
                .exclude(id=instance.id)
            )
            for index, topic in enumerate(related_topics, start=1):
                topic.sequence_number = index
                topic.save()


@receiver(post_save, sender=Chat)
def notify_user_on_response(sender, instance, created, **kwargs):
    text_uz = "Sizning xabaringizga javob berildi"
    text_ru = "Вашему сообщению был дан ответ"
    if instance.response and not created:
        Notification.objects.create(
            user=instance.user, message_uz=text_uz, message_ru=text_ru
        )
        instance.is_answered = True
        instance.save()
