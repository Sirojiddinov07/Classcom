from modeltranslation.translator import TranslationOptions, register

from core.apps.classcom.models import Science, ScienceTypes


@register(ScienceTypes)
class ScienceTypesScience(TranslationOptions):
    fields = ("name",)


@register(Science)
class ScienceTranslationOptions(TranslationOptions):
    fields = ("name",)
