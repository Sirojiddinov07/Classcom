from django.contrib import admin
from core.apps.classcom.models import Resource
from modeltranslation.admin import TabbedTranslationAdmin


@admin.register(Resource)
class ResourceAdmin(TabbedTranslationAdmin):
    list_display = (
        "name",
        "description",
    )
    search_fields = (
        "name",
    )
