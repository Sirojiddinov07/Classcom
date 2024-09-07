from django.contrib import admin
from unfold.admin import ModelAdmin

from core.apps.classcom.models import Download


@admin.register(Download)
class DownloadAdmin(ModelAdmin):
    list_display = (
        "id",
        "user",
        "date",
        "media",
    )
