from modeltranslation.translator import register, TranslationOptions
from core.apps.classcom.models import Science


@register(Science)
class ScienceTranslationOptions(TranslationOptions):
    fields = ("name",)
