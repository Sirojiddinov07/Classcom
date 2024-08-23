from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from core.apps.classcom import models, serializers


class ScienceViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    queryset = models.Science.objects.all().order_by("order_number")
    serializer_class = serializers.ScienceSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["science_grp", "name"]

    def get_queryset(self):
        queryset = models.Science.objects.all()
        class_group = self.request.query_params.get('class_group', None)
        if class_group is not None:
            queryset = queryset.filter(class_group=class_group)
        return queryset


class ScienceTypesViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = serializers.ScienceTypesSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["name"]
    http_method_names = ["get"]

    def get_queryset(self):
        queryset = models.ScienceTypes.objects.all()
        science_id = self.request.query_params.get('science', None)
        class_group = self.request.query_params.get('class_group', None)
        if science_id is not None:
            queryset = queryset.filter(science__id=science_id)
        if class_group is not None:
            queryset = queryset.filter(science__class_group=class_group)
        return queryset
