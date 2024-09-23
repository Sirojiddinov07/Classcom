from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from modeltranslation.admin import TabbedTranslationAdmin
from unfold.admin import ModelAdmin

from core.http import models, resources


@admin.register(models.Region)
class RegionAdmin(ModelAdmin, TabbedTranslationAdmin):
    list_display = ["id", "region"]
    search_fields = ["region"]


@admin.register(models.District)
class DistrictAdmin(ModelAdmin, TabbedTranslationAdmin):
    list_display = ["id", "region", "district"]
    search_fields = ["region__region", "district"]


@admin.register(models.ScienceGroups)
class ScienceGroupsAdmin(
    ModelAdmin, ImportExportModelAdmin, TabbedTranslationAdmin
):
    resource_class = resources.ScienceGroupsResource
    list_display = ["id", "name"]
    search_fields = ["name"]
