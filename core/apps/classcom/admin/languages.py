from django.contrib import admin

from core.apps.classcom.choices import LanguageModel


@admin.register(LanguageModel)
class LanguageModelAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "language",
    )
    search_fields = ("language",)
    fieldsets = ((None, {"fields": ("language",)}),)
