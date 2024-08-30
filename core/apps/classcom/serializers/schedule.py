from datetime import date

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from core.apps.classcom.models import ScheduleChoices, Quarter, Weeks
from core.apps.classcom.models.schedule import Schedule, ScheduleTemplate
from core.apps.classcom.serializers import (
    QuarterMiniSerializer,
    ScienceSerializer,
    ClassesSerializer,
    ClassTypeSerializer,
)
from core.apps.classcom.serializers.weks import WeeksSerializer
from core.http.serializers import UserSerializer, ClassGroupSerializer


############################################
# Schedule Serializer
############################################
class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = (
            "id",
            "shift",
            "science",
            "classes",
            "class_type",
            "weekday",
            "start_time",
            "end_time",
            "lesson_time",
            "class_group",
        )


############################################
# Schedule List Serializer
############################################
class ScheduleListSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    science = ScienceSerializer()
    classes = ClassesSerializer()
    class_type = ClassTypeSerializer()
    class_group = ClassGroupSerializer()

    class Meta:
        model = Schedule
        fields = (
            "id",
            "shift",
            "user",
            "science",
            "classes",
            "class_type",
            "weekday",
            "start_time",
            "end_time",
            "lesson_time",
            "class_group",
        )


############################################
# Schedule Template Serializer
############################################
class ScheduleTemplateSerializer(serializers.ModelSerializer):
    schedules = ScheduleSerializer(many=True)

    class Meta:
        model = ScheduleTemplate
        fields = (
            "id",
            "name",
            "schedules",
        )

    def create(self, validated_data):
        user = self.context["request"].user
        schedules_data = validated_data.pop("schedules")

        if ScheduleTemplate.objects.filter(user=user).exists():
            schedule_template = ScheduleTemplate.objects.create(
                user=user, **validated_data
            )
            for schedule_data in schedules_data:
                schedule = Schedule.objects.create(user=user, **schedule_data)
                schedule_template.schedules.add(schedule)
            return schedule_template

        schedule_template = ScheduleTemplate.objects.create(
            user=user, **validated_data
        )
        for schedule_data in schedules_data:
            schedule = Schedule.objects.create(user=user, **schedule_data)
            schedule_template.schedules.add(schedule)

        current_date = date.today()

        quarter = Quarter.objects.filter(
            start_date__lte=current_date, end_date__gte=current_date
        ).first()

        if not quarter:
            raise ValidationError("No quarter found for the current date.")

        weeks = Weeks.objects.filter(quarter=quarter)

        for week in weeks:
            ScheduleChoices.objects.create(
                user=user,
                schedule_template=schedule_template,
                quarter=quarter,
                week=week,
            )

        return schedule_template

    def update(self, instance, validated_data):
        user = self.context["request"].user
        schedules_data = validated_data.pop("schedules")
        instance.name = validated_data.get("name", instance.name)
        instance.user = user
        instance.save()

        # Delete schedules that are not in the update data
        schedule_ids = [
            schedule_data.get("id")
            for schedule_data in schedules_data
            if schedule_data.get("id")
        ]
        for schedule in instance.schedules.exclude(id__in=schedule_ids):
            schedule.delete()

        # Update or create schedules
        for schedule_data in schedules_data:
            schedule_id = schedule_data.get("id")
            if schedule_id:
                schedule = Schedule.objects.get(id=schedule_id)
                for attr, value in schedule_data.items():
                    setattr(schedule, attr, value)
                schedule.save()
            else:
                schedule = Schedule.objects.create(user=user, **schedule_data)
                instance.schedules.add(schedule)

        return instance


############################################
# Schedule Template List Serializer
############################################
class ScheduleTemplateListSerializer(serializers.ModelSerializer):
    schedules = ScheduleListSerializer(many=True)
    user = UserSerializer()

    class Meta:
        model = ScheduleTemplate
        fields = (
            "id",
            "user",
            "name",
            "schedules",
        )


############################################
# Schedule Choice List Serializer
############################################
class ScheduleChoiceListSerializer(serializers.ModelSerializer):
    schedule_template = ScheduleTemplateListSerializer()
    quarter = QuarterMiniSerializer()
    week = WeeksSerializer()

    class Meta:
        model = ScheduleChoices
        fields = (
            "id",
            "schedule_template",
            "quarter",
            "week",
            "created_at",
        )


############################################
# Schedule Choice Serializer
############################################
class ScheduleChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduleChoices
        fields = (
            "id",
            "schedule_template",
            "quarter",
            "week",
            "created_at",
        )

    def create(self, validated_data):
        user = self.context["request"].user
        schedule_template = validated_data.get("schedule_template")
        quarter = validated_data.get("quarter")
        week = validated_data.get("week")
        schedule_choice = ScheduleChoices.objects.create(
            user=user,
            schedule_template=schedule_template,
            quarter=quarter,
            week=week,
        )
        return schedule_choice
