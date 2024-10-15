from django.db.models import Q
from django_filters import FilterSet, NumberFilter, CharFilter

from ..models import Resource


class ResourceFilter(FilterSet):
    type = NumberFilter(field_name="type", lookup_expr="exact")
    search = CharFilter(method="filter_by_all_fields")

    class Meta:
        model = Resource
        fields = ("type", "search")

    def filter_by_all_fields(self, queryset, name, value):  # noqa
        return queryset.filter(
            Q(name__icontains=value)
            | Q(description__icontains=value)
            | Q(category__name__icontains=value)
            | Q(category_type__name__icontains=value)
            | Q(type__name__icontains=value)
        )
