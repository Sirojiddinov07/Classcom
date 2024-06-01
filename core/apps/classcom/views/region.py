from rest_framework import viewsets, permissions

from core.apps.classcom.serializers import RegionSerializer
from core.http.choices import Region


class RegionViewSet(viewsets.ModelViewSet):
    queryset = Region.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegionSerializer
