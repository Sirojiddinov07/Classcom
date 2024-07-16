from django.contrib import admin
from core.apps.classcom.models import Settings


@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    list_display = (
        "key",
        "value",
    )
    search_fields = (
        "key",
        "value",
    )
