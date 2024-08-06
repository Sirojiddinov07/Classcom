from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from modeltranslation.admin import TabbedTranslationAdmin

from core.apps.classcom.models import Science, ScienceTypes


@admin.register(ScienceTypes)
class ScienceTypesAdmin(ImportExportModelAdmin, TabbedTranslationAdmin):
    list_display = ("id", "name")


@admin.register(Science)
class ScienceAdmin(ImportExportModelAdmin, TabbedTranslationAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
