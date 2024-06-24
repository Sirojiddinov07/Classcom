from rest_framework import viewsets, permissions

from core.apps.classcom.serializers import RegionSerializer
from core.http import models


class RegionViewSet(viewsets.ModelViewSet):
    queryset = models.Region.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegionSerializer
    http_method_names = ["get"]
