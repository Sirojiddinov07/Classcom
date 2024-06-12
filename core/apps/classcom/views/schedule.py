from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
import json

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
    def get_empty_schedule(lesson_time):
        return {
            "lesson_time": str(lesson_time),
            "science": {
                "id": None,
                "name": None
            },
            "classes": {
                "id": None,
                "name": None
            },
            "start_time": None,
            "end_time": None,
        }

    for day in Weekday.choices:
        morning_schedule = [get_empty_schedule(i) for i in range(1, 7)]
        evening_schedule = [get_empty_schedule(i) for i in range(1, 7)]

        morning_schedules = Schedule.objects.filter(shift=ShiftChoice.MORNING, weekday=day[0]).order_by('lesson_time')
        for schedule in morning_schedules:
            lesson_time_index = int(schedule.lesson_time) - 1
            morning_schedule[lesson_time_index] = {
                "lesson_time": schedule.lesson_time,
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
            }

        evening_schedules = Schedule.objects.filter(shift=ShiftChoice.EVENING, weekday=day[0]).order_by('lesson_time')
        for schedule in evening_schedules:
            lesson_time_index = int(schedule.lesson_time) - 1
            evening_schedule[lesson_time_index] = {
                "lesson_time": schedule.lesson_time,
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
            }

        response_data.append({
            "id": day[0],
            "data": {
                "morning": morning_schedule,
                "evening": evening_schedule
            }
        })

    return JsonResponse(response_data, safe=False)



@method_decorator(csrf_exempt, name='dispatch')
class DayScheduleView(View):

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            weekday = data.get('weekday')

            response_data = {}

            # Default empty schedule object
            def get_empty_schedule(lesson_time):
                return {
                    "lesson_time": str(lesson_time),
                    "science": {
                        "id": None,
                        "name": None
                    },
                    "classes": {
                        "id": None,
                        "name": None
                    },
                    "start_time": None,
                    "end_time": None,
                }

            # Validate weekday
            weekday_choices = dict(Weekday.choices)
            if weekday not in weekday_choices:
                return JsonResponse({"error": "Invalid weekday"}, status=400)

            morning_schedule = [get_empty_schedule(i) for i in range(1, 7)]
            evening_schedule = [get_empty_schedule(i) for i in range(1, 7)]

            # Fetch and sort all morning schedules for the given weekday
            morning_schedules = Schedule.objects.filter(shift=ShiftChoice.MORNING, weekday=weekday).order_by('lesson_time')
            for schedule in morning_schedules:
                lesson_time_index = int(schedule.lesson_time) - 1
                morning_schedule[lesson_time_index] = {
                    "lesson_time": schedule.lesson_time,
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
                }

            # Fetch and sort all evening schedules for the given weekday
            evening_schedules = Schedule.objects.filter(shift=ShiftChoice.EVENING, weekday=weekday).order_by('lesson_time')
            for schedule in evening_schedules:
                lesson_time_index = int(schedule.lesson_time) - 1
                evening_schedule[lesson_time_index] = {
                    "lesson_time": schedule.lesson_time,
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
                }

            response_data = {
                "id": weekday,
                "data": {
                    "morning": morning_schedule,
                    "evening": evening_schedule
                }
            }

            return JsonResponse(response_data, safe=False)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)



@method_decorator(csrf_exempt, name='dispatch')
class RangeScheduleView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            start_day = data.get('start_day')
            end_day = data.get('end_day')

            # Validate weekdays
            weekday_choices = list(dict(Weekday.choices).keys())
            if start_day not in weekday_choices or end_day not in weekday_choices:
                return JsonResponse({"error": "Invalid weekday"}, status=400)

            start_index = weekday_choices.index(start_day)
            end_index = weekday_choices.index(end_day)
            if start_index > end_index:
                return JsonResponse({"error": "Start day must be before or the same as end day"}, status=400)

            response_data = []

            def get_empty_schedule(lesson_time):
                return {
                    "lesson_time": str(lesson_time),
                    "science": {
                        "id": None,
                        "name": None
                    },
                    "classes": {
                        "id": None,
                        "name": None
                    },
                    "start_time": None,
                    "end_time": None,
                }

            for i in range(start_index, end_index + 1):
                day = weekday_choices[i]
                morning_schedule = [get_empty_schedule(i) for i in range(1, 7)]
                evening_schedule = [get_empty_schedule(i) for i in range(1, 7)]

                morning_schedules = Schedule.objects.filter(shift=ShiftChoice.MORNING, weekday=day).order_by('lesson_time')
                for schedule in morning_schedules:
                    lesson_time_index = int(schedule.lesson_time) - 1
                    morning_schedule[lesson_time_index] = {
                        "lesson_time": schedule.lesson_time,
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
                    }

                evening_schedules = Schedule.objects.filter(shift=ShiftChoice.EVENING, weekday=day).order_by('lesson_time')
                for schedule in evening_schedules:
                    lesson_time_index = int(schedule.lesson_time) - 1
                    evening_schedule[lesson_time_index] = {
                        "lesson_time": schedule.lesson_time,
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
                    }

                response_data.append({
                    "id": day,
                    "data": {
                        "morning": morning_schedule,
                        "evening": evening_schedule
                    }
                })

            return JsonResponse(response_data, safe=False)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
