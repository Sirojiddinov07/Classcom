from modeltranslation.translator import TranslationOptions, register

from core.apps.classcom.models.electron_resource import (
    ElectronResourceCategory,
    ElectronResourceSubCategory,
)


@register(ElectronResourceCategory)
class ElectronResourceCategoryTranslationOptions(TranslationOptions):
    fields = ("name", "description")


@register(ElectronResourceSubCategory)
class ElectronResourceSubCategoryTranslationOptions(TranslationOptions):
    fields = ("name", "description")
