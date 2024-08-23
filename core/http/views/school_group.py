from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from core.http.models import ClassGroup
from core.http.serializers import ClassGroupSerializer


class FilteredSchoolGroupViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = ClassGroupSerializer
    http_method_names = ["get"]

    def get_queryset(self):
        queryset = ClassGroup.objects.all()

        return queryset
