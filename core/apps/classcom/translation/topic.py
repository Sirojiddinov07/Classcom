from modeltranslation.translator import TranslationOptions, register

from core.apps.classcom.models import Topic


@register(Topic)
class TopicTranslationOptions(TranslationOptions):
    fields = ("name",)
