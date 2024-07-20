from django.contrib import admin

from core.apps.classcom.models import Quarter


@admin.register(Quarter)
class QuarterAdmin(admin.ModelAdmin):
    list_display = (
        "choices",
        "start_date",
        "end_date",
    )
