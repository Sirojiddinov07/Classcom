from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin
from unfold.decorators import display

from core.apps.classcom.models import ChangeModeratorStatus, PlanAppeal


@admin.register(PlanAppeal)
class PlanAppealAdmin(ModelAdmin):
    list_display = (
        "id",
        "user",
        "show_status_customized_color",
        "created_at",
    )
    search_fields = (
        "user__first_name",
        "user__last_name",
    )
    list_filter = ("status",)
    filter_horizontal = (
        "science",
        "science_type",
        "classes",
        "class_groups",
        "tmr_files",
    )
    actions = ("accept", "reject")

    compressed_fields = True  # Default: False

    def accept(self, request, queryset):
        queryset.update(status=ChangeModeratorStatus.ACCEPTED)

    accept.short_description = _("Qabul qilish")

    def reject(self, request, queryset):
        queryset.update(status=ChangeModeratorStatus.REJECTED)

    reject.short_description = _("Rad etish")

    @display(
        description=_("Status"),
        ordering="status",
        label={
            ChangeModeratorStatus.ACCEPTED: "success",  # green
            ChangeModeratorStatus.PENDING: "warning",  # orange
            ChangeModeratorStatus.REJECTED: "danger",  # red
        },
    )
    def show_status_customized_color(self, obj):
        return obj.status, obj.get_status_display()
