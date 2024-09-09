from django.utils.translation import gettext_lazy as _
from unfold.contrib.filters.admin import DropdownFilter

from core.apps.classcom.models import Plan


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
            return queryset.filter(plans__id=self.value())
        return queryset
