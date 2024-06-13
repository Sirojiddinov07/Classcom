from rest_framework import viewsets
from core.apps.classcom import models
from core.apps.classcom import choices
from core.apps.classcom import serializers
from core.apps.classcom import permissions
from core.http import permissions as http_permissions
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator


class ResourceViewSet(viewsets.ModelViewSet):
    queryset = models.Resource.objects.all()

    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return serializers.ResourceCreateSerializer
        elif self.action == "retrieve":
            return serializers.ResourceDetailSerializer
        return serializers.ResourceSerializer
