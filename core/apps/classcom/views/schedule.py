from datetime import datetime

from rest_framework import viewsets

from core.apps.classcom.models import ScheduleChoices, Weeks
from core.apps.classcom.models.schedule import ScheduleTemplate
from core.apps.classcom.serializers import (
    ScheduleChoiceSerializer,
    ScheduleChoiceListSerializer,
    ScheduleTemplateListSerializer,
)
from core.apps.classcom.serializers import ScheduleTemplateSerializer


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

        if week_param or quarter_param:
            if week_param:
                queryset = queryset.filter(week=week_param)
            if quarter_param:
                queryset = queryset.filter(quarter=quarter_param)
        elif date_param:
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

        return queryset

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ScheduleChoiceListSerializer
        return ScheduleChoiceSerializer


############################################
# Schedule Template View
############################################
class ScheduleTemplateViewSet(viewsets.ModelViewSet):
    queryset = ScheduleTemplate.objects.all()
    serializer_class = ScheduleTemplateSerializer
    http_method_names = [
        "get",
        "post",
        "put",
        "patch",
        "delete",
    ]

    def get_queryset(self):
        return ScheduleTemplate.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ScheduleTemplateListSerializer
        return ScheduleTemplateSerializer
