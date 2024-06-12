from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, status
import json

from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView

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



class GetScheduleDataView(GenericAPIView, ListModelMixin):

    def get(self, request):
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

            response_data.append(
                {
                    "id": day[0],
                    "data": {
                        "morning": morning_schedule,
                        "evening": evening_schedule,
                    },
                }
            )

        return Response(response_data)

@method_decorator(csrf_exempt, name='dispatch')
class DayScheduleView(APIView):

    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            weekday = data.get('weekday')

            response_data = {}

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

            weekday_choices = dict(Weekday.choices)
            if weekday not in weekday_choices:
                return Response({"error": "Invalid weekday"}, status=status.HTTP_400_BAD_REQUEST)

            morning_schedule = [get_empty_schedule(i) for i in range(1, 7)]
            evening_schedule = [get_empty_schedule(i) for i in range(1, 7)]

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

            return Response(response_data)
        except json.JSONDecodeError:
            return Response({"error": "Invalid JSON"}, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_exempt, name='dispatch')
class RangeScheduleView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            start_day = data.get('start_day')
            end_day = data.get('end_day')

            weekday_choices = list(dict(Weekday.choices).keys())
            if start_day not in weekday_choices or end_day not in weekday_choices:
                return Response({"error": "Invalid weekday"}, status=status.HTTP_400_BAD_REQUEST)

            start_index = weekday_choices.index(start_day)
            end_index = weekday_choices.index(end_day)
            if start_index > end_index:
                return Response({"error": "Start day must be before or the same as end day"}, status=status.HTTP_400_BAD_REQUEST)

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

            return Response(response_data)
        except json.JSONDecodeError:
            return Response({"error": "Invalid JSON"}, status=status.HTTP_400_BAD_REQUEST)
