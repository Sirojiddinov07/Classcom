from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from core.apps.classcom import resources
from modeltranslation.admin import TabbedTranslationAdmin

from core.apps.classcom.models import Plan


@admin.register(Plan)
class PlanAdmin(ImportExportModelAdmin, TabbedTranslationAdmin):
    """
    Cosutimize the plan model in admin panel interface
    """

    resource_class = resources.PlanResource
