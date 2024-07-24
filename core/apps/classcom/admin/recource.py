from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin

from core.apps.classcom.models import Resource


@admin.register(Resource)
class ResourceAdmin(TabbedTranslationAdmin):
    list_display = (
        "name",
        "description",
    )
    search_fields = ("name",)
