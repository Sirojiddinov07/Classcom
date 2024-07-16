from django.contrib import admin

from core.apps.classcom import models
from modeltranslation.admin import TabbedTranslationAdmin


@admin.register(models.ResourceType)
class ResourceTypeAdmin(TabbedTranslationAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
