from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from import_export.admin import ImportExportModelAdmin

from core.apps.classcom import resources
from core.apps.classcom.models import Plan


@admin.register(Plan)
class PlanAdmin(ImportExportModelAdmin):
    list_display = ("id", "full_name", "created_at")
    """
    Customize the plan model in admin panel interface
    """

    resource_class = resources.PlanResource

    search_fields = (
        "user__first_name",
        "user__last_name",
        "user__phone",
    )
    filter_horizontal = ("topic",)

    def full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

    full_name.short_description = _("Ism Familiya")
