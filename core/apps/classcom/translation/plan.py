from modeltranslation.translator import register, TranslationOptions
from core.apps.classcom.models import Plan


@register(Plan)
class PlanTranslationOptions(TranslationOptions):
    fields = ("name", "description")
