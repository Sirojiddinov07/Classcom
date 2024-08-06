import json
from datetime import date, datetime

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from core.apps.classcom.choices import ShiftChoice, Weekday
from core.apps.classcom.models import Quarter, Schedule
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


class GetScheduleDataView(APIView):
    def get_empty_schedule(self, lesson_time):
        return {
            "lesson_time": str(lesson_time),
            "science": {"id": None, "name": None},
            "classes": {"id": None, "name": None},
            "start_time": None,
            "end_time": None,
        }

    def get(self, request):
        response_data = []

        # Get today's date
        today = date.today()

        # Find the quarter that includes today's date
        current_quarter = None
        quarters = Quarter.objects.all()
        for quarter in quarters:
            if quarter.start_date <= today <= quarter.end_date:
                current_quarter = quarter
                break

        if current_quarter is None:
            return Response({"No active quarter found for today's date."})

        quarter_data = {"quarter": current_quarter.choices, "days": []}

        for day in Weekday.choices:
            morning_schedule = [
                self.get_empty_schedule(i) for i in range(1, 7)
            ]
            evening_schedule = [
                self.get_empty_schedule(i) for i in range(1, 7)
            ]

            morning_schedules = Schedule.objects.filter(
                shift=ShiftChoice.MORNING,
                weekday=day[0],
                quarter=current_quarter,
                user=request.user,
            ).order_by("lesson_time")

            for schedule in morning_schedules:
                lesson_time_index = int(schedule.lesson_time) - 1
                morning_schedule[lesson_time_index] = {
                    "id": schedule.id,
                    "lesson_time": schedule.lesson_time,
                    "science": {
                        "id": schedule.science.id,
                        "name": schedule.science.name,
                    },
                    "classes": {
                        "id": schedule.classes.id,
                        "name": schedule.classes.name,
                    },
                    "start_time": schedule.start_time.strftime("%H:%M"),
                    "end_time": schedule.end_time.strftime("%H:%M"),
                }

            evening_schedules = Schedule.objects.filter(
                shift=ShiftChoice.EVENING,
                weekday=day[0],
                quarter=current_quarter,
                user=request.user,
            ).order_by("lesson_time")
            for schedule in evening_schedules:
                lesson_time_index = int(schedule.lesson_time) - 1
                evening_schedule[lesson_time_index] = {
                    "id": schedule.id,
                    "lesson_time": schedule.lesson_time,
                    "science": {
                        "id": schedule.science.id,
                        "name": schedule.science.name,
                    },
                    "classes": {
                        "id": schedule.classes.id,
                        "name": schedule.classes.name,
                    },
                    "start_time": schedule.start_time.strftime("%H:%M"),
                    "end_time": schedule.end_time.strftime("%H:%M"),
                }

            quarter_data["days"].append(
                {
                    "id": day[0].lower(),
                    "name": day[1],
                    "data": {
                        "morning": morning_schedule,
                        "evening": evening_schedule,
                    },
                }
            )

        response_data.append(quarter_data)
        return Response(response_data)


@method_decorator(csrf_exempt, name="dispatch")
class DayScheduleView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            date_str = data.get("date")

            if not date_str:
                return Response(
                    {"error": "Date field is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            try:
                date = datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                return Response(
                    {"error": "Invalid date format. Use YYYY-MM-DD."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Check if the requested date is a Sunday
            if date.strftime("%A").lower() == "sunday":
                return Response(
                    {"message": "This day is Sunday."},
                    status=status.HTTP_200_OK,
                )

            try:
                quarter_instance = Quarter.objects.get(
                    start_date__lte=date, end_date__gte=date
                )
            except Quarter.DoesNotExist:
                return Response(
                    {"error": "No quarter found for the given date."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            weekday = date.strftime("%A").lower()

            # Initialize empty schedules
            morning_schedule = [
                self.get_empty_schedule(i) for i in range(1, 7)
            ]
            evening_schedule = [
                self.get_empty_schedule(i) for i in range(1, 7)
            ]

            morning_schedules = Schedule.objects.filter(
                shift=ShiftChoice.MORNING,
                weekday=weekday,
                quarter=quarter_instance,
                user=request.user,
            ).order_by("lesson_time")
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
                    "start_time": schedule.start_time.strftime("%H:%M"),
                    "end_time": schedule.end_time.strftime("%H:%M"),
                }

            evening_schedules = Schedule.objects.filter(
                shift=ShiftChoice.EVENING,
                weekday=weekday,
                quarter=quarter_instance,
                user=request.user,
            ).order_by("lesson_time")
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
                    "start_time": schedule.start_time.strftime("%H:%M"),
                    "end_time": schedule.end_time.strftime("%H:%M"),
                }

            response_data = {
                "date": date_str,
                "quarter": quarter_instance.choices,
                "weekday": weekday,
                "morning": morning_schedule,
                "evening": evening_schedule,
            }

            return Response(response_data)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def get_empty_schedule(self, lesson_time):
        return {
            "lesson_time": str(lesson_time),
            "science": {"id": None, "name": None},
            "classes": {"id": None, "name": None},
            "start_time": None,
            "end_time": None,
        }


@method_decorator(csrf_exempt, name="dispatch")
class RangeScheduleView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            start_day = data.get("start_day")
            end_day = data.get("end_day")
            quarter = data.get("quarter")  # Added quarter parameter

            weekday_choices = dict(Weekday.choices)
            if (
                start_day not in weekday_choices
                or end_day not in weekday_choices
            ):
                return Response(
                    {"error": "Invalid weekday"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            start_index = list(weekday_choices.keys()).index(start_day)
            end_index = list(weekday_choices.keys()).index(end_day)
            if start_index > end_index:
                return Response(
                    {
                        "error": "Start day must be before or the same as end \
                            day"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            response_data = []

            def get_empty_schedule(lesson_time):
                return {
                    "lesson_time": str(lesson_time),
                    "science": {"id": None, "name": None},
                    "classes": {"id": None, "name": None},
                    "start_time": None,
                    "end_time": None,
                }

            for i in range(start_index, end_index + 1):
                day = list(weekday_choices.keys())[i]
                morning_schedule = [get_empty_schedule(i) for i in range(1, 7)]
                evening_schedule = [get_empty_schedule(i) for i in range(1, 7)]

                morning_schedules = Schedule.objects.filter(
                    shift=ShiftChoice.MORNING,
                    weekday=day,
                    quarter=quarter,
                    user=request.user,
                ).order_by("lesson_time")
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
                        "start_time": schedule.start_time.strftime("%H:%M"),
                        "end_time": schedule.end_time.strftime("%H:%M"),
                    }

                evening_schedules = Schedule.objects.filter(
                    shift=ShiftChoice.EVENING,
                    weekday=day,
                    quarter=quarter,
                    user=request.user,
                ).order_by("lesson_time")
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
                        "start_time": schedule.start_time.strftime("%H:%M"),
                        "end_time": schedule.end_time.strftime("%H:%M"),
                    }

                response_data.append(
                    {
                        "id": day,
                        "data": {
                            "morning": morning_schedule,
                            "evening": evening_schedule,
                        },
                    }
                )

            return Response(response_data)

        except json.JSONDecodeError:
            return Response(
                {"error": "Invalid JSON"}, status=status.HTTP_400_BAD_REQUEST
            )
