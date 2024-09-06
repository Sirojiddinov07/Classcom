from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin
from unfold.admin import ModelAdmin

from core.apps.classcom import models


@admin.register(models.ResourceType)
class ResourceTypeAdmin(ModelAdmin, TabbedTranslationAdmin):
    list_display = ("id", "order_number", "name", "type", "created_at")
    search_fields = ("name",)
