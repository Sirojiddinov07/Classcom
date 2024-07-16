from modeltranslation.translator import register, TranslationOptions
from core.apps.classcom.models import Classes


@register(Classes)
class ClassesTranslationOptions(TranslationOptions):
    fields = ("name",)
