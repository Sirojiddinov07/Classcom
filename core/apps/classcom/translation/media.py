from modeltranslation.translator import TranslationOptions, register

from core.apps.classcom.models import Media


@register(Media)
class MediaTranslationOptions(TranslationOptions):
    fields = ("name", "desc")
