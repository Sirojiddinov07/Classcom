from django_filters import FilterSet, NumberFilter
from ..models import Resource


class ResourceFilter(FilterSet):
    type = NumberFilter(field_name="type", lookup_expr="exact")

    class Meta:
        model = Resource
        fields = ("type",)
