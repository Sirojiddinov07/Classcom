from modeltranslation.translator import TranslationOptions, register

from core.apps.classcom.models import Classes


@register(Classes)
class ClassesTranslationOptions(TranslationOptions):
    fields = ("name",)
