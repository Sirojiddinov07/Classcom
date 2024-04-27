from django.contrib import admin
from import_export import admin as import_export
from core.http import models


class GroupAdmin(import_export.ImportExportModelAdmin):
    list_display = ['name']
    search_fields = ["name"]
    filter_horizontal = (
        "permissions",
    )


@admin.register(models.User)
class UserAdmin(import_export.ImportExportModelAdmin):
    list_display = ['phone', "first_name", "last_name"]
    search_fields = ["phone", "first_name", "last_name"]
    filter_horizontal = (
        "groups",
        "user_permissions",
    )
