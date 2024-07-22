from modeltranslation.translator import TranslationOptions, register

from core.apps.classcom.models import Notification


@register(Notification)
class NotificationTranslationOptions(TranslationOptions):
    fields = ("message",)
