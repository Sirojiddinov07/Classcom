from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from core.apps.classcom import models, serializers


class ScienceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Science.objects.all()
    serializer_class = serializers.ScienceSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["science_grp", "name"]