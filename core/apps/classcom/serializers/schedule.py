from rest_framework import serializers

from core.apps.classcom.models import Schedule
from core.apps.classcom.serializers.classes import ClassesSerializer
from core.apps.classcom.serializers.science import ScienceSerializer
from core.http.serializers import UserSerializer


############################################
# Schedule List Serializer
############################################
class ScheduleListSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    science = ScienceSerializer()
    classes = ClassesSerializer()

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
            "date",
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
            "quarter",
            "date",
        )

    def create(self, validated_data):
        user = self.context["request"].user
        schedule = Schedule.objects.create(user=user, **validated_data)

        return schedule
