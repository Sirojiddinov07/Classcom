from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin

from core.apps.classcom.models import Teacher


@admin.register(Teacher)
class TeacherAdmin(ModelAdmin):
    list_display = (
        "id",
        "user",
        "payment_status",
    )
    search_fields = (
        "user__first_name",
        "user__last_name",
        "user__phone",
        "science__name",
    )
    list_filter = (
        "payment_status",
        "science",
    )
    filter_horizontal = ("science",)

    def user(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

    user.short_description = _("Foydalanuvchi")
