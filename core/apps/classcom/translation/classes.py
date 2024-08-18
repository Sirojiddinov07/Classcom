from modeltranslation.translator import TranslationOptions, register

from core.apps.classcom.models import Classes, ClassType


@register(Classes)
class ClassesTranslationOptions(TranslationOptions):
    fields = ("name",)


@register(ClassType)
class ClassTypeTranslationOptions(TranslationOptions):
    fields = ("name",)
