from django.contrib import admin
from unfold.admin import ModelAdmin

from core.apps.classcom.models import Settings


@admin.register(Settings)
class SettingsAdmin(ModelAdmin):
    list_display = (
        "id",
        "key",
        "value",
    )
    search_fields = (
        "key",
        "value",
    )
