from rest_framework import viewsets
from core.apps.classcom.models import Schedule
from core.apps.classcom.serializers import ScheduleCreateSerializer, ScheduleListSerializer


class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']

    def get_queryset(self):
        return Schedule.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ScheduleListSerializer
        return ScheduleCreateSerializer
