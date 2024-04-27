from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from core.http import choices
from core.http import resources


@admin.register(choices.Region)
class RegionAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = resources.RegionResource
    list_display = ['id', 'region']
    search_fields = ['region']


@admin.register(choices.District)
class DistrictAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = resources.DistrictResource
    list_display = ['id', 'region', 'district']
    search_fields = ['region', 'district']


@admin.register(choices.ScienceGroups)
class ScienceGroupsAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = resources.ScienceGroupsResource
    list_display = ['name']
    search_fields = ['name']
