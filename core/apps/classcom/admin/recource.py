from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from modeltranslation.admin import TabbedTranslationAdmin
from unfold.admin import ModelAdmin

from core.apps.classcom.models import Resource


@admin.register(Resource)
class ResourceAdmin(ModelAdmin, TabbedTranslationAdmin):
    list_display = (
        "id",
        "order_number",
        "full_name",
        "name",
        "description",
    )
    search_fields = (
        "name",
        "user__first_name",
        "user__last_name",
        "user__phone",
    )
    ordering = ("order_number",)
    filter_horizontal = ("media",)
    autocomplete_fields = (
        "user",
        "media",
        "category",
        "category_type",
        "type",
        "classes",
        "science",
    )

    def full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

    full_name.short_description = _("Ism Familiya")
