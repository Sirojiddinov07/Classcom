from modeltranslation.translator import TranslationOptions, register

from core.apps.classcom.choices import LanguageModel


@register(LanguageModel)
class LanguageModelTranslationOptions(TranslationOptions):
    fields = ["name"]
