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
        school_type_id = self.request.query_params.get("school_type")
        science_id = self.request.query_params.get("science")

        if school_type_id:
            queryset = queryset.filter(school_type_id=school_type_id)
        if science_id:
            queryset = queryset.filter(science_id=science_id)

        return queryset
