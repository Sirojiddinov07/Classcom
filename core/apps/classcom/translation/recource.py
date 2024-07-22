from modeltranslation.translator import TranslationOptions, register

from core.apps.classcom.models import Resource


@register(Resource)
class ResourceTranslationOptions(TranslationOptions):
    fields = ("name", "description")
