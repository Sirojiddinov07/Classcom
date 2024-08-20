from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from import_export.admin import ImportExportModelAdmin
from modeltranslation.admin import TabbedTranslationAdmin

from core.apps.classcom import resources
from core.apps.classcom.models import Plan


@admin.register(Plan)
class PlanAdmin(ImportExportModelAdmin, TabbedTranslationAdmin):
    list_display = ("id", "full_name", "name", "description", "created_at")
    """
    Cosutimize the plan model in admin panel interface
    """

    resource_class = resources.PlanResource

    search_fields = (
        "name",
        "user__first_name",
        "user__last_name",
        "user__phone",
    )

    def full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

    full_name.short_description = _("Ism Familiya")
