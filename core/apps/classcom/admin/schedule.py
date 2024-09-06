from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin

from core.apps.classcom.models import (
    Schedule,
    ScheduleChoices,
    ScheduleTemplate,
)


@admin.register(Schedule)
class ScheduleAdmin(ModelAdmin):
    list_display = (
        "id",
        "user",
        "science",
        "classes",
        "weekday",
        "start_time",
        "end_time",
    )

    search_fields = ("user__first_name", "user__last_name", "science__name")

    list_filter = ("weekday",)

    def classes(self, obj):
        return obj.science.name

    classes.short_description = _("Fan")

    def user(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

    user.short_description = _("Foydalanuvchi")


@admin.register(ScheduleChoices)
class ScheduleChoicesAdmin(ModelAdmin):
    list_display = ("id", "user", "quarter", "week")
    search_fields = ("user__first_name", "user__last_name", "schedule__name")
    list_filter = ("week", "quarter")


@admin.register(ScheduleTemplate)
class ScheduleTemplateAdmin(ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
    list_filter = ("name",)
