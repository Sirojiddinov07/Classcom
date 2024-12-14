from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin

from core.apps.classcom.models import DaysOff


@admin.register(DaysOff)
class DaysOffAdmin(ModelAdmin):
    list_display = (
        "id",
        "full_name",
        "from_date",
        "to_date",
        "reason",
    )
    search_fields = (
        "user__first_name",
        "user__last_name",
        "user__phone",
        "reason",
    )
    filter_horizontal = ("science", "_class")
    autocomplete_fields = ("user", "science", "_class")

    def full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

    full_name.short_description = _("Ism Familiya")
