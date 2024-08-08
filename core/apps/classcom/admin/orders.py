from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from core.apps.classcom.models import Orders


@admin.register(Orders)
class OrdersAdmin(ImportExportModelAdmin):
    list_display = ("id", "status", "price")
