from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import Plans, Payments, Orders


@admin.register(Orders)
class OrdersAdmin(ModelAdmin):
    list_display = (
        "id",
        "user",
        "status",
        "price",
        "start_date",
        "created_at",
    )
    search_fields = (
        "user__first_name",
        "user__last_name",
        "user__phone",
    )
    filter_horizontal = ("types",)
    list_filter = ("status",)


@admin.register(Payments)
class PaymentsAdmin(ModelAdmin):
    list_display = (
        "id",
        "order",
        "price",
        "status",
        "trans_id",
    )
    search_fields = (
        "order__user__first_name",
        "order__user__last_name",
        "order__user__phone",
        "order__plan__name",
        "trans_id",
    )
    list_filter = ("status",)


@admin.register(Plans)
class PlansAdmin(ModelAdmin):
    list_display = (
        "id",
        "quarter",
        "price",
    )
    search_fields = ("price",)
    ordering = ("quarter",)
    list_filter = ("quarter",)
