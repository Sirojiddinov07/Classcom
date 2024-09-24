from rest_framework import permissions, viewsets
from rest_framework.pagination import PageNumberPagination

from core.apps.classcom.serializers import RegionSerializer
from core.http import models


class CustomPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = "page_size"
    max_page_size = 100


class RegionViewSet(viewsets.ModelViewSet):
    queryset = models.Region.objects.all().order_by("region")
    permission_classes = [permissions.AllowAny]
    serializer_class = RegionSerializer
    http_method_names = ["get"]
    pagination_class = CustomPagination
