from datetime import date

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from core.apps.classcom.choices import ShiftChoice, Weekday
from core.apps.classcom.models import Quarter, Schedule, ScheduleChoices
from core.apps.classcom.serializers import (
    ScheduleCreateSerializer,
    ScheduleListSerializer,
    ScheduleChoiceSerializer,
    ScheduleChoiceListSerializer,
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


class GetScheduleDataView(APIView):
    def get_empty_schedule(self, lesson_time, date=None):
        return {
            "lesson_time": str(lesson_time),
            "science": {"id": None, "name": None},
            "classes": {"id": None, "name": None},
            "start_time": None,
            "end_time": None,
            "date": date,  # Add date field
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
                self.get_empty_schedule(i, today) for i in range(1, 7)
            ]
            evening_schedule = [
                self.get_empty_schedule(i, today) for i in range(1, 7)
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
                    "date": schedule.date,  # Add date field
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
                    "date": schedule.date,  # Add date field
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


############################################
# Schedule Choice View
############################################
class ScheduleChoiceViewSet(viewsets.ModelViewSet):
    queryset = ScheduleChoices.objects.all()
    http_method_names = ["get", "post", "put", "patch", "delete"]

    def get_queryset(self):
        queryset = ScheduleChoices.objects.filter(user=self.request.user)
        quarter_param = self.request.query_params.get("quarter")
        week_param = self.request.query_params.get("week")

        if quarter_param:
            queryset = queryset.filter(quarter=quarter_param)
        if week_param:
            queryset = queryset.filter(week=week_param)

        return queryset

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ScheduleChoiceListSerializer
        return ScheduleChoiceSerializer
