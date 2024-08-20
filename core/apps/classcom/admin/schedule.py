from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from core.apps.classcom.models import Schedule


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "science",
        "classes",
        "weekday",
        "start_time",
        "end_time",
        "quarter",
    )

    search_fields = ("user__first_name", "user__last_name", "science__name")

    list_filter = ("quarter", "weekday")

    def classes(self, obj):
        return obj.science.name

    classes.short_description = _("Fan")

    def user(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

    user.short_description = _("Foydalanuvchi")
