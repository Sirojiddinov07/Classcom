from modeltranslation.translator import register, TranslationOptions
from core.apps.classcom.models import Topic


@register(Topic)
class TopicTranslationOptions(TranslationOptions):
    fields = ("name",)
