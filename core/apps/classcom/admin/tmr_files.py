from django.contrib import admin
from unfold.admin import ModelAdmin

from core.apps.classcom.models import TmrFiles


@admin.register(TmrFiles)
class TmrFilesAdmin(ModelAdmin):
    list_display = ("id", "title", "description", "file", "type", "size")
    search_fields = ("title", "description", "file", "type")
    list_filter = ("is_active", "type")
    readonly_fields = ("size", "type")
