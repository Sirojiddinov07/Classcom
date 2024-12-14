from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin
from unfold.admin import ModelAdmin

from core.apps.classcom.models import Science, ScienceTypes


@admin.register(ScienceTypes)
class ScienceTypesAdmin(ModelAdmin, TabbedTranslationAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Science)
class ScienceAdmin(ModelAdmin, TabbedTranslationAdmin):
    list_display = ("id", "order_number", "name", "class_group")
    search_fields = ("name",)
    ordering = ("order_number",)
    list_filter = ("types",)
    filter_horizontal = ("types",)
    autocomplete_fields = ("science_grp", "types", "class_group")
