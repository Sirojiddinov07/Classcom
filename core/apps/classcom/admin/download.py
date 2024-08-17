from django.contrib import admin

from core.apps.classcom.models import Download


@admin.register(Download)
class DownloadAdmin(admin.ModelAdmin):
    list_display = (
        "teacher",
        "moderator",
        "date",
        "media",
    )
