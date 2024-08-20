from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from modeltranslation.admin import TabbedTranslationAdmin

from core.apps.classcom.models import Classes, ClassType


@admin.register(Classes)
class ClassesAdmin(ImportExportModelAdmin, TabbedTranslationAdmin):
    list_display = ("id", "name", "type")
    search_fields = ("name",)


@admin.register(ClassType)
class ClassTypeAdmin(ImportExportModelAdmin, TabbedTranslationAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
