from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, viewsets
from django_filters import rest_framework as filters

from core.apps.classcom import models, serializers


class ResourceFilter(filters.FilterSet):
    category_name = filters.CharFilter(field_name='category__name', lookup_expr='icontains')
    category_type_name = filters.CharFilter(field_name='category__category_type__name', lookup_expr='icontains')

    class Meta:
        model = models.Resource
        fields = ['name', 'type', 'classes', 'category_name', 'category_type_name']

class ResourceViewSet(viewsets.ModelViewSet):
    queryset = models.Resource.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ResourceFilter

    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        match self.action:
            case "create" | "update" | "partial_update":
                return serializers.ResourceCreateSerializer
            case "retrieve":
                return serializers.ResourceDetailSerializer
        return serializers.ResourceSerializer
