from rest_framework import viewsets

from core.apps.classcom.serializers import DistrictSerializer
from core.http.choices import District


class DistrictViewSet(viewsets.ModelViewSet):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer