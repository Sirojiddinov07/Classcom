from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin
from unfold.admin import ModelAdmin

from core.apps.classcom.filters import UserFilter
from core.apps.classcom.models import Media


@admin.register(Media)
class MediaAdmin(ModelAdmin, TabbedTranslationAdmin):
    list_display = (
        "id",
        "name",
        "file",
        "type",
        "count",
        "statistics",
    )
    search_fields = ("name",)
    list_display_links = ("name",)
    list_filter = ("type", "object_type", UserFilter)
    list_filter_submit = True
    readonly_fields = ("created_at", "updated_at")
    filter_horizontal = ("download_users",)
    autocomplete_fields = ("download_users", "user")
