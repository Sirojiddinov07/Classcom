from modeltranslation.translator import TranslationOptions, register

from core.apps.classcom.models import Science


@register(Science)
class ScienceTranslationOptions(TranslationOptions):
    fields = ("name",)
