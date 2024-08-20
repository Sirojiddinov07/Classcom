from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from core.http.models import SchoolType
from core.http.serializers import SchoolTypeSerializer


class SchoolTypeViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = SchoolTypeSerializer
    http_method_names = ["get"]

    def get_queryset(self):
        queryset = SchoolType.objects.all()
        institution = self.request.query_params.get("institution", None)
        if institution:
            queryset = queryset.filter(institution=institution)
        return queryset
