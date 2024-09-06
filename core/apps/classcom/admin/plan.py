from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin

from core.apps.classcom.models import Plan


@admin.register(Plan)
class PlanAdmin(ModelAdmin):
    list_display = (
        "id",
        "full_name",
        "classes",
        "science",
        "class_group",
        "science_types",
        "quarter",
        "created_at",
    )
    """
    Customize the plan model in admin panel interface
    """

    search_fields = (
        "user__first_name",
        "user__last_name",
        "user__phone",
    )
    filter_horizontal = ("topic",)

    def full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

    full_name.short_description = _("Ism Familiya")

    def classes(self, obj):
        return f"{obj.classes.name}"

    classes.short_description = _("Sinflar")

    def science(self, obj):
        return f"{obj.science.name}"

    science.short_description = _("Fan")

    def class_group(self, obj):
        return f"{obj.class_group.name}"

    class_group.short_description = _("Sinflar turi")

    def science_types(self, obj):
        return f"{obj.science_types.name}"

    science_types.short_description = _("Fan turi")

    def quarter(self, obj):
        return f"{obj.quarter.name}"

    quarter.short_description = _("Chorak")
