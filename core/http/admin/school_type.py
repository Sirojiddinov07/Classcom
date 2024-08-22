from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin

from core.http.models import SchoolType, ClassGroup


class CustomTabbedTranslationAdmin(TabbedTranslationAdmin, admin.ModelAdmin):
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
        "school_type",
        "science",
        "created_at",
        "updated_at",
    ]
    search_fields = ["name"]
    list_filter = ["school_type", "science"]
    autocomplete_fields = ["school_type", "science"]
