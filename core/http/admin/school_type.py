from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin
from unfold.admin import ModelAdmin

from core.http.models import SchoolType, ClassGroup


class CustomTabbedTranslationAdmin(TabbedTranslationAdmin, ModelAdmin):
    pass


@admin.register(SchoolType)
class SchoolTypeAdmin(CustomTabbedTranslationAdmin):
    list_display = ["id", "name", "created_at", "updated_at"]
    search_fields = ["name"]


@admin.register(ClassGroup)
class ClassGroupAdmin(CustomTabbedTranslationAdmin):
    list_display = [
        "id",
        "name",
        "created_at",
        "updated_at",
    ]
    search_fields = ["name"]
