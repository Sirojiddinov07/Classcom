from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin

from core.apps.classcom.models import Media


@admin.register(Media)
class MediaAdmin(TabbedTranslationAdmin):
    list_display = (
        "name",
        "desc",
        "file",
    )
    search_fields = ("name",)
    list_filter = ("type",)
    readonly_fields = ("created_at", "updated_at")
