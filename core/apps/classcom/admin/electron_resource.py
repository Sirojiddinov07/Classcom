from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin
from unfold.admin import ModelAdmin

from core.apps.classcom.models.electron_resource import (
    ElectronResource,
    ElectronResourceCategory,
    ElectronResourceSubCategory,
)


@admin.register(ElectronResourceCategory)
class ElectronResourceCategoryAdmin(ModelAdmin, TabbedTranslationAdmin):
    list_display = ("id", "name", "description")
    search_fields = ("name", "description")


@admin.register(ElectronResourceSubCategory)
class ElectronResourceSubCategoryAdmin(ModelAdmin, TabbedTranslationAdmin):
    list_display = ("id", "name", "description", "category")
    search_fields = ("name", "description", "category__name")
    autocomplete_fields = ("category",)


@admin.register(ElectronResource)
class ElectronResourceAdmin(ModelAdmin):
    list_display = ("id", "name", "description", "category")
    search_fields = ("name", "description", "category__name")
    autocomplete_fields = ("category", "user")
    readonly_fields = ("name", "type", "size", "created_at")
