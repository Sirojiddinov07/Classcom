from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin
from unfold.admin import ModelAdmin

from core.apps.classcom.models import Category, CategoryType


@admin.register(Category)
class CategoryAdmin(ModelAdmin, TabbedTranslationAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(CategoryType)
class CategoryTypeAdmin(ModelAdmin, TabbedTranslationAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
