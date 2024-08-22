from modeltranslation.translator import TranslationOptions, register

from core.http.models import SchoolType, ClassGroup


@register(SchoolType)
class SchoolTypeTranslationOptions(TranslationOptions):
    fields = ("name",)


@register(ClassGroup)
class ClassGroupTranslationOptions(TranslationOptions):
    fields = ("name",)
