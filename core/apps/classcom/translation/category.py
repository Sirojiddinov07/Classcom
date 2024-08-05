from modeltranslation.translator import TranslationOptions, register

from core.apps.classcom.models import Category, CategoryType


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ("name",)




@register(CategoryType)
class CategoryTypeTranslationOptions(TranslationOptions):
    fields = ("name",)



