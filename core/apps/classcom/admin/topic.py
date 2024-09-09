from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from unfold.admin import ModelAdmin

from core.apps.classcom.filters import PlanFilter
from core.apps.classcom.models import Topic
from core.apps.classcom.resources import TopicResource


@admin.register(Topic)
class TopicAdmin(ModelAdmin, ImportExportModelAdmin):
    """Topic admin

    Args:
        ImportExportModelAdmin (_type_): _description_
    """

    resource_class = TopicResource
    list_filter_submit = True
    list_display = (
        "id",
        "sequence_number",
        "name",
        "description",
        "hours",
        "weeks",
        "media_creatable",
    )
    search_fields = (
        "name",
        "description",
    )
    filter_horizontal = ("media",)
    list_filter = (PlanFilter, "media_creatable")
