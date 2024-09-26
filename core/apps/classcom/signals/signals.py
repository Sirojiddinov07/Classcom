from django.db.models.signals import post_save, pre_delete, m2m_changed
from django.dispatch import receiver

from core.apps.websocket.models.notification import Notification
from core.http.models import User, ContractStatus
from ..models import Topic, Plan, Chat, Moderator
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
        Chat.objects.filter(pk=instance.pk).update(is_answered=True)


@receiver(
    m2m_changed, sender=User.document.through
)  # M2M relationship changes
def file_status_m2m(sender, instance, action, **kwargs):
    if action == "post_add":  # Trigger after documents are added
        if (
            instance.document.exists()
            and instance.status_file == ContractStatus.NO_FILE
        ):
            instance.status_file = ContractStatus.WAITING
            instance.save()
            Notification.objects.create(
                user=instance,
                message_uz="Sizning hujjatingiz qabul qilindi",
                message_ru="Ваш документ принят",
            )


@receiver(post_save, sender=User)
def file_status_pre_save(sender, instance, **kwargs):
    if instance.response_file:
        User.objects.filter(pk=instance.pk).update(
            status_file=ContractStatus.ACCEPTED, status=True
        )
        if Moderator.objects.filter(user=instance).exists():
            Moderator.objects.filter(user=instance).update(status=True)
        Notification.objects.create(
            user=instance,
            message_uz="Shartnoma qabul qilindi",
            message_ru="Договор принят",
        )
