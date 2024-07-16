from modeltranslation.translator import TranslationOptions, register

from core.apps.classcom.models import ResourceType


@register(ResourceType)
class ResourceTypeTranslationOptions(TranslationOptions):
    fields = ("name",)
