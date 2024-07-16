from modeltranslation.translator import register, TranslationOptions
from core.apps.classcom.models import Notification


@register(Notification)
class NotificationTranslationOptions(TranslationOptions):
    fields = ("message",)
