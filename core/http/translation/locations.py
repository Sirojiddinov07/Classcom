from modeltranslation.translator import TranslationOptions, register

from core.http.models.locations import District, Region


@register(Region)
class RegionTranslationOptions(TranslationOptions):
    fields = ("region",)


@register(District)
class DistrictTranslationOptions(TranslationOptions):
    fields = ("district",)
