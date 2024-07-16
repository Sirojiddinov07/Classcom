from modeltranslation.translator import register, TranslationOptions
from core.apps.classcom.models import Media


@register(Media)
class MediaTranslationOptions(TranslationOptions):
    fields = ("name", "desc")
