from django.contrib import admin
from unfold.admin import ModelAdmin

from core.apps.classcom.choices import LanguageModel


@admin.register(LanguageModel)
class LanguageModelAdmin(ModelAdmin):
    list_display = (
        "id",
        "language",
        "name",
    )
    search_fields = ("language",)
    fieldsets = ((None, {"fields": ("language", "name")}),)
