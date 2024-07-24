from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from core.apps.classcom import models, serializers


class ScienceViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    queryset = models.Science.objects.all()
    serializer_class = serializers.ScienceSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["science_grp", "name"]