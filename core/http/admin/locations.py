from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from core.http import resources, models


@admin.register(models.Region)
class RegionAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = resources.RegionResource
    list_display = ["id", "region"]
    search_fields = ["region"]


@admin.register(models.District)
class DistrictAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = resources.DistrictResource
    list_display = ["id", "region", "district"]
    search_fields = ["region", "district"]


@admin.register(models.ScienceGroups)
class ScienceGroupsAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = resources.ScienceGroupsResource
    list_display = ["name"]
    search_fields = ["name"]
