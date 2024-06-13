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

    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user)

        class_id = self.request.query_params.get("class_id")
        if class_id:
            queryset = queryset.filter(classes__id=class_id)

        search_term = self.request.query_params.get("search", None)
        if search_term:
            queryset = queryset.filter(
                name__icontains=search_term
            ) | queryset.filter(media__description__icontains=search_term)

        return queryset



    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


    def get_serializer_class(self):
        match self.action:
            case "create" | "update" | "partial_update":
                return serializers.ResourceCreateSerializer
            case "retrieve":
                return serializers.ResourceDetailSerializer
        return serializers.ResourceSerializer
