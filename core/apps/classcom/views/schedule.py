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
    response_data = []

    # Default empty schedule object
    empty_schedule = {
        "id": None,
        "science": {"id": None, "name": None},
        "classes": {"id": None, "name": None},
        "start_time": None,
        "end_time": None,
        "lesson_time": None,
    }

    # Initialize response data structure
    for day in Weekday.choices:
        morning_schedule = []
        evening_schedule = []

        # Fetch all morning schedules for the current weekday
        morning_schedules = list(
            Schedule.objects.filter(shift=ShiftChoice.MORNING, weekday=day[0])
        )
        for i in range(6):  # Ensure there are exactly 6 time slots
            if i < len(morning_schedules):
                schedule = morning_schedules[i]
                morning_schedule.append(
                    {
                        "id": schedule.id,
                        "science": {
                            "id": schedule.science.id,
                            "name": schedule.science.name,
                        },
                        "classes": {
                            "id": schedule.classes.id,
                            "name": schedule.classes.name,
                        },
                        "start_time": schedule.start_time,
                        "end_time": schedule.end_time,
                        "lesson_time": schedule.lesson_time,
                    }
                )
            else:
                morning_schedule.append(
                    empty_schedule
                )  # Append default empty schedule

        # Fetch all evening schedules for the current weekday
        evening_schedules = list(
            Schedule.objects.filter(shift=ShiftChoice.EVENING, weekday=day[0])
        )
        for i in range(6):  # Ensure there are exactly 6 time slots
            if i < len(evening_schedules):
                schedule = evening_schedules[i]
                evening_schedule.append(
                    {
                        "id": schedule.id,
                        "science": {
                            "id": schedule.science.id,
                            "name": schedule.science.name,
                        },
                        "classes": {
                            "id": schedule.classes.id,
                            "name": schedule.classes.name,
                        },
                        "start_time": schedule.start_time,
                        "end_time": schedule.end_time,
                        "lesson_time": schedule.lesson_time,
                    }
                )
            else:
                evening_schedule.append(
                    empty_schedule
                )  # Append default empty schedule

        response_data.append(
            {
                "id": day[0],
                "data": {
                    "morning": morning_schedule,
                    "evening": evening_schedule,
                },
            }
        )

    return JsonResponse(response_data, safe=False)
