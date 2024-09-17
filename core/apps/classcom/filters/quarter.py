from django.utils.translation import gettext_lazy as _
from unfold.contrib.filters.admin import DropdownFilter

from core.apps.classcom.models import Quarter, Science, Classes
from core.http.models import ClassGroup


class QuarterFilter(DropdownFilter):
    title = _("Chorak")
    parameter_name = "quarter"

    def lookups(self, request, model_admin):
        quarters = Quarter.objects.all()
        return [
            (
                quarter.id,
                f"{quarter.choices} {quarter.start_date}-{quarter.end_date}",
            )
            for quarter in quarters
        ]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(quarter__id=self.value())
        return queryset


class ScienceFilter(DropdownFilter):
    title = _("Fan")
    parameter_name = "science"

    def lookups(self, request, model_admin):
        sciences = Science.objects.all()
        return [(science.id, science.name) for science in sciences]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(science__id=self.value())
        return queryset


class ClassesFilter(DropdownFilter):
    title = _("Sinflar")
    parameter_name = "classes"

    def lookups(self, request, model_admin):
        classes2 = Classes.objects.all()
        return [(classes.id, classes.name) for classes in classes2]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(classes__id=self.value())
        return queryset


class ClassGroupFilter(DropdownFilter):
    title = _("Sinflar guruhi")
    parameter_name = "class_group"

    def lookups(self, request, model_admin):
        class_groups = ClassGroup.objects.all()
        return [
            (class_group.id, class_group.name) for class_group in class_groups
        ]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(class_group__id=self.value())
        return queryset
