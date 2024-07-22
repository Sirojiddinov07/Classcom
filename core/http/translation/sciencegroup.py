from modeltranslation.translator import TranslationOptions, register

from core.http.models.science import ScienceGroups


@register(ScienceGroups)
class ScienceGroupsTranslationOptions(TranslationOptions):
    fields = ("name",)
