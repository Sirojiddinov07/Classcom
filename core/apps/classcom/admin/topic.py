from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from unfold.admin import ModelAdmin

from core.apps.classcom.models import Topic
from core.apps.classcom.resources import TopicResource


# from unfold.contrib.import_export.forms import ExportForm, ImportForm


@admin.register(Topic)
class TopicAdmin(ModelAdmin, ImportExportModelAdmin):
    # import_form_class = ImportForm
    # export_form_class = ExportForm
    # export_form_class = SelectableFieldsExportForm
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
