from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from core.apps.classcom import models, serializers


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
    fields = ["name", "type", "classes", "category", "category_type"]

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

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)

        if "category_type" in self.request.query_params:
            all_classes = models.Classes.objects.all()

            filtered_resources = queryset

            filtered_class_ids = filtered_resources.values_list(
                "classes_id", flat=True
            )
            classes_not_in_filtered_resources = all_classes.exclude(
                id__in=filtered_class_ids
            )

            self.extra_context = {
                "resources": filtered_resources,
                "classes_not_in_filtered_resources": classes_not_in_filtered_resources,
            }
        else:
            self.extra_context = {}
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        classes_serializer = serializers.ClassesSerializer(
            self.extra_context.get("classes_not_in_filtered_resources", []),
            many=True,
        )

        response_data = {
            "resources": serializer.data,
            "classes_not_in_filtered_resources": classes_serializer.data,
        }

        return Response(response_data)
