from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from core.http.models import SchoolType
from core.http.serializers import SchoolTypeSerializer


class SchoolTypeViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = SchoolType.objects.all()
    serializer_class = SchoolTypeSerializer
    http_method_names = ["get"]
