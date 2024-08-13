from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from core.apps.classcom import models, serializers
from ..filters import ResourceFilter


class ResourceTypesViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=["GET"], url_path="resource-types")
    def get(self, request):
        """
        Resource Turlarini olish uchun GET request
        """
        resource_types = models.ResourceType.objects.all()
        serializer = serializers.ResourceTypeSerializer(
            resource_types, many=True
        )
        return Response(serializer.data)


class ResourceViewSet(viewsets.ModelViewSet):
    queryset = models.Resource.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ResourceFilter
    # fields = ["name", "type", "classes", "subtype", "category", "category_type"]

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

