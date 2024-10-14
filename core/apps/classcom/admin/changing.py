from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin
from unfold.decorators import display

from core.apps.classcom.models import ChangeModeratorStatus
from core.apps.classcom.models.changing import ChangeModerator


@admin.register(ChangeModerator)
class ChangeModeratorAdmin(ModelAdmin):
    list_display = (
        "id",
        "get_user",
        "show_status_customized_color",
        "created_at",
    )
    search_fields = (
        "user__first_name",
        "user__last_name",
    )
    list_filter = ("status",)
    readonly_fields = (
        "get_user",
        "get_science",
        "get_science_type",
        "get_classes",
        "get_class_groups",
    )

    actions = ("accept", "reject")
    fieldsets = (
        (
            _("Asosiy ma'lumotlar"),
            {
                "classes": ["tab"],
                "fields": (
                    "get_user",
                    "status",
                ),
            },
        ),
        (
            _("Fanlar"),
            {
                "classes": ["tab"],
                "fields": (
                    "get_science",
                    "get_science_type",
                ),
            },
        ),
        (
            _("Sinflar"),
            {
                "classes": ["tab"],
                "fields": (
                    "get_classes",
                    "get_class_groups",
                ),
            },
        ),
    )

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

    def get_user(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}, {obj.user.phone}"

    get_user.short_description = _("Foydalanuvchi")

    def get_science(self, obj):
        return f"{obj.science.name}"

    get_science.short_description = _("Fan")

    def get_science_type(self, obj):
        return ", ".join(
            [science_type.name for science_type in obj.science_type.all()]
        )

    get_science_type.short_description = _("Fan turi")

    def get_classes(self, obj):
        return f"{obj.classes.name}"

    get_classes.short_description = _("Sinflar")

    def get_class_groups(self, obj):
        return f"{obj.class_groups.name}"

    get_class_groups.short_description = _("Sinf guruhlari")
