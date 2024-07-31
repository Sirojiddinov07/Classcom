from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from modeltranslation.admin import TabbedTranslationAdmin

from core.apps.classcom.models import Category, CategoryType


@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin, TabbedTranslationAdmin):
    list_display = ("id", "name", "category_type")
    search_fields = ("name",)



@admin.register(CategoryType)
class CategoryTypeAdmin(ImportExportModelAdmin, TabbedTranslationAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
