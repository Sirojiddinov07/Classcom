from typing import Callable, TypeVar, cast, Protocol

from django.contrib import admin
from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin

from core.apps.classcom.filters import (
    QuarterFilter,
    ClassesFilter,
    ScienceFilter,
    ClassGroupFilter,
)
from core.apps.classcom.models import Plan


class ActionWithDescription(Protocol):
    def __call__(
        self,
        modeladmin: admin.ModelAdmin,
        request: HttpRequest,
        queryset: QuerySet,
    ) -> None: ...

    short_description: str


T = TypeVar("T", bound=Callable[..., None])


def describe_action(action: T, description: str) -> ActionWithDescription:
    casted_action = cast(ActionWithDescription, action)
    casted_action.short_description = description
    return casted_action


@admin.register(Plan)
class PlanAdmin(ModelAdmin):
    list_display = (
        "id",
        "full_name",
        "classes",
        "science",
        "class_group",
        "science_types",
        "quarter",
        "created_at",
        "is_active",
    )
    list_editable = ("is_active",)
    list_filter_submit = True
    list_filter = (
        QuarterFilter,
        ScienceFilter,
        ClassesFilter,
        ClassGroupFilter,
    )
    actions = ["make_inactive", "make_active"]
    """
    Customize the plan model in admin panel interface
    """

    search_fields = (
        "user__first_name",
        "user__last_name",
        "user__phone",
    )
    filter_horizontal = ("topic",)

    def full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

    full_name.short_description = _("Ism Familiya")

    def classes(self, obj):
        return f"{obj.classes.name}"

    classes.short_description = _("Sinflar")

    def science(self, obj):
        return f"{obj.science.name}"

    science.short_description = _("Fan")

    def class_group(self, obj):
        return f"{obj.class_group.name}"

    class_group.short_description = _("Sinflar turi")

    def science_types(self, obj):
        return f"{obj.science_types.name}"

    science_types.short_description = _("Fan turi")

    def quarter(self, obj):
        return f"{obj.quarter.name}"

    quarter.short_description = _("Chorak")

    def make_active(self, request, queryset):
        queryset.update(is_active=True)

    make_active = describe_action(
        make_active, _("Faol qilish")
    )  # Apply custom type

    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)

    make_inactive = describe_action(
        make_inactive, _("Nofaol qilish")
    )  # Apply custom type
