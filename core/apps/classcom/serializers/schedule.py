from rest_framework import serializers

from core.apps.classcom.models import Classes, Schedule, Science, Topic
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
    topic = serializers.CharField(read_only=True)

    class Meta:
        model = Schedule
        fields = (
            "id",
            "shift",
            "user",
            "science",
            "topic",
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
    # topic = serializers.PrimaryKeyRelatedField(queryset=Topic.objects.all(), required=True)
    topic = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = Schedule
        fields = (
            "shift",
            "science",
            "topic",
            "classes",
            "weekday",
            "start_time",
            "end_time",
            "lesson_time",
            "quarter",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        initial_data = kwargs.get("data", {})
        science_id = initial_data.get("science")
        if science_id:
            self.fields["topic"].queryset = Topic.objects.filter(
                science_id=science_id
            )

    # def create(self, validated_data):
    #     user = self.context["request"].user
    #     topic = validated_data.pop('topic', None)
    #     return Schedule.objects.create(user=user, **validated_data)
    def create(self, validated_data):
        user = self.context["request"].user
        validated_data.pop("topic")
        schedule = Schedule.objects.create(user=user, **validated_data)

        return schedule
