from django.contrib import admin
from django.utils.translation import gettext_lazy as _
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
        "plan_id",
    )
    search_fields = (
        "name",
        "description",
    )
    list_editable = ("media_creatable",)
    filter_horizontal = ("media",)
    autocomplete_fields = ("plan_id", "user", "media")
    list_filter = (PlanFilter, "media_creatable")
    actions = ["make_inactive", "make_active"]

    def make_inactive(self, request, queryset):
        """Make selected topics inactive

        Args:
            request (_type_): _description_
            queryset (_type_): _description_
        """
        queryset.update(media_creatable=False)

    make_inactive.short_description = _("Nofaol qilish")

    def make_active(self, request, queryset):
        """Make selected topics active

        Args:
            request (_type_): _description_
            queryset (_type_): _description_
        """
        queryset.update(media_creatable=True)

    make_active.short_description = _("Faol qilish")
