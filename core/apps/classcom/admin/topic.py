from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from modeltranslation.admin import TabbedTranslationAdmin

from core.apps.classcom.models import Topic


@admin.register(Topic)
class TopicAdmin(ImportExportModelAdmin, TabbedTranslationAdmin):
    """Topic admin

    Args:
        ImportExportModelAdmin (_type_): _description_
    """

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
