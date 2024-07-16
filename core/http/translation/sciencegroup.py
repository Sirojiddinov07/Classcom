from modeltranslation.translator import register, TranslationOptions
from core.http.models.science import ScienceGroups


@register(ScienceGroups)
class ScienceGroupsTranslationOptions(TranslationOptions):
    fields = ("name",)