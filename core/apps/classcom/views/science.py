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


class ScienceTypesViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    queryset = models.ScienceTypes.objects.all()
    serializer_class = serializers.ScienceTypesSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["name"]
    http_method_names = ["get"]
