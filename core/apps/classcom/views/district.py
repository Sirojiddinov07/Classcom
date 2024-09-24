from rest_framework import mixins, permissions, viewsets

from core.apps.classcom.serializers import RegionDetailSerializer
from core.apps.classcom.views.region import CustomPagination
from core.http import models


class DistrictViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = models.Region.objects.all().order_by("districts")
    serializer_class = RegionDetailSerializer
    pagination_class = CustomPagination
