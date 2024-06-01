from rest_framework import viewsets, permissions

from core.apps.classcom.serializers import DistrictSerializer
from core.http.choices import District


class DistrictViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = District.objects.all()
    serializer_class = DistrictSerializer