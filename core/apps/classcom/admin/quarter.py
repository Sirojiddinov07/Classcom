from django.contrib import admin
from unfold.admin import ModelAdmin

from core.apps.classcom.models import Quarter


@admin.register(Quarter)
class QuarterAdmin(ModelAdmin):
    list_display = (
        "id",
        "choices",
        "start_date",
        "end_date",
    )
