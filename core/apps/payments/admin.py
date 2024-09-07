from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import Plans, Payments, Orders


@admin.register(Orders)
class OrdersAdmin(ModelAdmin):
    list_display = (
        "id",
        "user",
        "status",
        "created_at",
        "updated_at",
    )
    search_fields = (
        "user__first_name",
        "user__last_name",
        "user__phone",
    )
    filter_horizontal = ("types",)


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
    )


@admin.register(Plans)
class PlansAdmin(ModelAdmin):
    list_display = (
        "id",
        "quarter",
        "price",
    )
    search_fields = (
        "quarter__name",
        "price",
    )
    ordering = ("quarter",)
