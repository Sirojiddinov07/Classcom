from django.utils.translation import gettext_lazy as _
from unfold.contrib.filters.admin import DropdownFilter

from core.apps.classcom.models import Plan
from core.http.models import User


class PlanFilter(DropdownFilter):
    title = _("Tematik reja")
    parameter_name = "plan"

    def lookups(self, request, model_admin):
        plans = Plan.objects.all()
        return [
            (
                plan.id,
                f"{plan.science.name} - {plan.science_types.name} - {plan.classes.name} - {plan.class_group.name}",
            )
            for plan in plans
        ]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(plan_id__id=self.value())
        return queryset


# User filter
class UserFilter(DropdownFilter):
    title = _("Foydalanuvchi")
    parameter_name = "user"

    def lookups(self, request, model_admin):
        users = User.objects.all()
        return [
            (
                user.id,
                f"ID:{user.id}-{user.phone} - {user.first_name} {user.last_name} {user.father_name}",
            )
            for user in users
        ]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(user_id__id=self.value())
        return queryset
