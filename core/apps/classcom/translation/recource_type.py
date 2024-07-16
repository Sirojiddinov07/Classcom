from modeltranslation.translator import register, TranslationOptions
from core.apps.classcom.models import ResourceType


@register(ResourceType)
class ResourceTypeTranslationOptions(TranslationOptions):
    fields = ("name",)
