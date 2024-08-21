from rest_framework import serializers

from core.apps.classcom.models import Schedule, ScheduleChoices
from core.apps.classcom.serializers import (
    ClassTypeSerializer,
    QuarterMiniSerializer,
)
from core.apps.classcom.serializers.classes import ClassesSerializer
from core.apps.classcom.serializers.science import ScienceSerializer
from core.apps.classcom.serializers.weks import WeeksSerializer
from core.http.serializers import UserSerializer


############################################
# Schedule List Serializer
############################################
class ScheduleListSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    science = ScienceSerializer()
    classes = ClassesSerializer()
    class_type = ClassTypeSerializer()

    class Meta:
        model = Schedule
        fields = (
            "id",
            "name",
            "shift",
            "user",
            "science",
            "classes",
            "class_type",
            "weekday",
            "start_time",
            "end_time",
            "lesson_time",
        )


############################################
# Schedule Create Serializer
############################################
class ScheduleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = (
            "name",
            "shift",
            "science",
            "classes",
            "class_type",
            "weekday",
            "start_time",
            "end_time",
            "lesson_time",
        )

    def create(self, validated_data):
        user = self.context["request"].user
        schedule = Schedule.objects.create(user=user, **validated_data)

        return schedule


############################################
# Schedule Choice Serializer
############################################
class ScheduleChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduleChoices
        fields = (
            "id",
            "schedule",
            "quarter",
            "week",
            "created_at",
        )

    def create(self, validated_data):
        user = self.context["request"].user
        schedule_choice = ScheduleChoices.objects.create(
            user=user, **validated_data
        )

        return schedule_choice


############################################
# Schedule Choice List Serializer
############################################
class ScheduleChoiceListSerializer(serializers.ModelSerializer):
    schedule = ScheduleListSerializer()
    quarter = QuarterMiniSerializer()
    week = WeeksSerializer()

    class Meta:
        model = ScheduleChoices
        fields = (
            "id",
            "schedule",
            "quarter",
            "week",
            "created_at",
        )
