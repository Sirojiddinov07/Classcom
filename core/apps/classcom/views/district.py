from rest_framework import viewsets, permissions

from core.apps.classcom.serializers import RegionDetailSerializer
from core.http import models
from rest_framework import mixins

class DistrictViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = models.Region.objects.all()
    serializer_class = RegionDetailSerializer

