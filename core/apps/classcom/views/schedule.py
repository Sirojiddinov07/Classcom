from datetime import datetime

from rest_framework import viewsets

from core.apps.classcom.models import Schedule
from core.apps.classcom.models import ScheduleChoices, Weeks
from core.apps.classcom.serializers import (
    ScheduleChoiceSerializer,
    ScheduleChoiceListSerializer,
)
from core.apps.classcom.serializers import (
    ScheduleCreateSerializer,
    ScheduleListSerializer,
)


class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    http_method_names = ["get", "post", "put", "patch", "delete"]

    def get_queryset(self):
        queryset = Schedule.objects.filter(user=self.request.user)
        date_param = self.request.query_params.get("date")
        if date_param:
            queryset = queryset.filter(date=date_param)
        return queryset

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ScheduleListSerializer
        return ScheduleCreateSerializer


############################################
# Schedule Choice View
############################################
class ScheduleChoiceViewSet(viewsets.ModelViewSet):
    queryset = ScheduleChoices.objects.all()
    http_method_names = ["get", "post", "put", "patch", "delete"]

    def get_queryset(self):
        queryset = ScheduleChoices.objects.filter(user=self.request.user)
        date_param = self.request.query_params.get("date")
        quarter_param = self.request.query_params.get("quarter")
        week_param = self.request.query_params.get("week")

        if date_param:
            try:
                date = datetime.strptime(date_param, "%Y-%m-%d").date()
                week = Weeks.objects.filter(
                    start_date__lte=date, end_date__gte=date
                ).first()
                if week:
                    queryset = queryset.filter(week=week)
                else:
                    queryset = ScheduleChoices.objects.none()
            except ValueError:
                return ScheduleChoices.objects.none()

        if quarter_param:
            queryset = queryset.filter(quarter=quarter_param)
        if week_param:
            queryset = queryset.filter(week=week_param)

        return queryset

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ScheduleChoiceListSerializer
        return ScheduleChoiceSerializer
