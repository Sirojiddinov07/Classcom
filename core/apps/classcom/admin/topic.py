from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from modeltranslation.admin import TabbedTranslationAdmin

from core.apps.classcom.models import Topic
from core.apps.classcom.resources import TopicResource


@admin.register(Topic)
class TopicAdmin(ImportExportModelAdmin, TabbedTranslationAdmin):
    """Topic admin

    Args:
        ImportExportModelAdmin (_type_): _description_
    """

    resource_class = TopicResource
    list_display = (
        "id",
        "name",
        "description",
        "sequence_number",
    )
    search_fields = (
        "name",
        "description",
    )
    filter_horizontal = ("media",)
