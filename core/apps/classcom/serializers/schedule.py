from rest_framework import serializers
from core.apps.classcom.models import Schedule, Science, Classes
from core.http.models import User


class ScheduleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name", "last_name")


class ScheduleScienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Science
        fields = ("name",)


class ScheduleClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classes
        fields = ("name",)


############################################
# Schedule List Serializer
############################################


class ScheduleListSerializer(serializers.ModelSerializer):
    user = ScheduleUserSerializer()
    science = ScheduleScienceSerializer()
    classes = ScheduleClassSerializer()

    class Meta:
        model = Schedule
        fields = (
            "id",
            "shift",
            "user",
            "science",
            "classes",
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
            "shift",
            "science",
            "classes",
            "weekday",
            "start_time",
            "end_time",
            "lesson_time",
        )

    def create(self, validated_data):
        user = self.context["request"].user
        return Schedule.objects.create(user=user, **validated_data)
