from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from modeltranslation.admin import TabbedTranslationAdmin

from core.http import models, resources


@admin.register(models.Region)
class RegionAdmin(ImportExportModelAdmin, TabbedTranslationAdmin):
    resource_class = resources.RegionResource
    list_display = ["id", "region"]
    search_fields = ["region"]


@admin.register(models.District)
class DistrictAdmin(ImportExportModelAdmin, TabbedTranslationAdmin):
    resource_class = resources.DistrictResource
    list_display = ["id", "region", "district"]
    search_fields = ["region", "district"]


@admin.register(models.ScienceGroups)
class ScienceGroupsAdmin(ImportExportModelAdmin, TabbedTranslationAdmin):
    resource_class = resources.ScienceGroupsResource
    list_display = ["id", "name"]
    search_fields = ["name"]
