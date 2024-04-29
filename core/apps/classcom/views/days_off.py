from rest_framework import viewsets
from core.apps.classcom.models import DaysOff
from core.apps.classcom.serializers import DaysOffSerializer


class DaysOffViewSet(viewsets.ModelViewSet):
    queryset = DaysOff.objects.all()
    serializer_class = DaysOffSerializer

    def get_queryset(self):
        user = self.request.user
        return DaysOff.objects.filter(user=user)
