from modeltranslation.translator import TranslationOptions, register

from core.apps.classcom.models import Plan


@register(Plan)
class PlanTranslationOptions(TranslationOptions):
    fields = ("name", "description")
