from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin

from core.http.models import SchoolType


class CustomTabbedTranslationAdmin(TabbedTranslationAdmin, admin.ModelAdmin):
    pass


@admin.register(SchoolType)
class SchoolTypeAdmin(CustomTabbedTranslationAdmin):
    list_display = ["id", "name", "created_at", "updated_at"]
    search_fields = ["name"]
