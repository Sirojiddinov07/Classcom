from django.contrib import admin

from core.apps.classcom.models import Schedule


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "science",
        "classes",
        "weekday",
        "start_time",
        "end_time",
        "quarter",
    )
