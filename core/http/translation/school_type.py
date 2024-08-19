from modeltranslation.translator import TranslationOptions, register

from core.http.models import SchoolType


@register(SchoolType)
class SchoolTypeTranslationOptions(TranslationOptions):
    fields = ("name",)
