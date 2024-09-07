from django.contrib import admin
from unfold.admin import ModelAdmin

from core.apps.classcom.models import Document


@admin.register(Document)
class DocumentAdmin(ModelAdmin):
    list_display = ("title", "description", "file", "type", "size")
    search_fields = ("title", "description", "file", "type")
    list_filter = ("is_active", "type")
    readonly_fields = ("size", "type")
