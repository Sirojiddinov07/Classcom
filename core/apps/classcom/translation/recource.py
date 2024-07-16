from modeltranslation.translator import register, TranslationOptions
from core.apps.classcom.models import Resource


@register(Resource)
class ResourceTranslationOptions(TranslationOptions):
    fields = ("name", "description")
