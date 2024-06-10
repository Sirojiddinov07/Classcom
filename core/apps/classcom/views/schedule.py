from django.http import JsonResponse
from rest_framework import viewsets

from core.apps.classcom.choices import Weekday, ShiftChoice
from core.apps.classcom.models import Schedule
from core.apps.classcom.serializers import (
    ScheduleCreateSerializer,
    ScheduleListSerializer,
)


class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    http_method_names = ["get", "post", "put", "patch", "delete"]

    def get_queryset(self):
        return Schedule.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ScheduleListSerializer
        return ScheduleCreateSerializer


def get_schedule_data(request):
    schedules = Schedule.objects.all()
    response_data = {}

    # Initialize response data structure
    for day in Weekday.choices:
        response_data[day[0]] = {
            "morning": [],
            "evening": []
        }

    # Populate response data
    for schedule in schedules:
        shift_key = 'morning' if schedule.shift == ShiftChoice.MORNING else 'evening'
        weekday_key = schedule.weekday
        response_data[weekday_key][shift_key].append({
            "id": schedule.id,
            "user": schedule.user.id,
            "science": schedule.science.id,
            "classes": schedule.classes.id,
            "start_time": schedule.start_time,
            "end_time": schedule.end_time,
            "lesson_time": schedule.lesson_time,
        })

    # Format the response
    formatted_response = [
        {"id": day[0], "data": response_data[day[0]]} for day in Weekday.choices
    ]

    return JsonResponse(formatted_response, safe=False)
