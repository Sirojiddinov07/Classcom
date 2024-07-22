from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin

from core.apps.classcom import models


@admin.register(models.ResourceType)
class ResourceTypeAdmin(TabbedTranslationAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
