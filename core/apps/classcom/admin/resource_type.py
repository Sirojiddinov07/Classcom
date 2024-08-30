from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin

from core.apps.classcom import models


@admin.register(models.ResourceType)
class ResourceTypeAdmin(TabbedTranslationAdmin):
    list_display = ("id", "order_number", "name", "type", "created_at")
    search_fields = ("name",)
