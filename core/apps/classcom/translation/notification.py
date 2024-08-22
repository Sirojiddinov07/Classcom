from modeltranslation.translator import TranslationOptions, register

from core.apps.websocket.models import Notification


@register(Notification)
class NotificationTranslationOptions(TranslationOptions):
    fields = ("message",)
