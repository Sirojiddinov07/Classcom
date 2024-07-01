from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from rest_framework import viewsets

from core.apps.classcom import models, serializers


class ResourceViewSet(viewsets.ModelViewSet):
    queryset = models.Resource.objects.all()

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
