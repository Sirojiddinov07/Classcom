from rest_framework import serializers

from core.apps.classcom.models import ChangeModerator
from core.apps.classcom.serializers import (
    ScienceSerializer,
    ClassesSerializer,
    ScienceTypesSerializer,
)
from core.http.serializers import ClassGroupSerializer


class ChangeModeratorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChangeModerator
        fields = ("id", "science", "science_type", "classes", "class_groups")

    def create(self, validated_data):
        user = self.context["request"].user
        science_types = validated_data.pop("science_type")
        instance = ChangeModerator.objects.create(**validated_data, user=user)
        instance.science_type.set(science_types)
        return instance


class ChangeModeratorDetailSerializer(serializers.ModelSerializer):
    science = ScienceSerializer()
    classes = ClassesSerializer()
    class_groups = ClassGroupSerializer()
    science_type = ScienceTypesSerializer(many=True)

    class Meta:
        model = ChangeModerator
        fields = (
            "id",
            "user",
            "status",
            "science",
            "science_type",
            "classes",
            "class_groups",
        )
