from modeltranslation.translator import register, TranslationOptions

from core.http.models.locations import Region, District


@register(Region)
class RegionTranslationOptions(TranslationOptions):
    fields = ("region",)


@register(District)
class DistrictTranslationOptions(TranslationOptions):
    fields = ("district",)
