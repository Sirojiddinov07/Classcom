from django.contrib import admin

from core.apps.classcom.models import DaysOff


@admin.register(DaysOff)
class DaysOffAdmin(admin.ModelAdmin):
    list_display = (
        "from_date",
        "to_date",
        "reason",
    )
