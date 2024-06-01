from rest_framework import viewsets

from core.apps.classcom.serializers import RegionSerializer
from core.http.choices import Region


class RegionViewSet(viewsets.ModelViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
