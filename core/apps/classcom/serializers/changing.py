from rest_framework import serializers

from core.apps.classcom.models import ChangeModerator
from core.apps.classcom.serializers import (
    ScienceSerializer,
    ScienceTypesSerializer,
    ClassesSerializer,
)
from core.http.serializers import ClassGroupSerializer


class ChangeModeratorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChangeModerator
        fields = ("id", "science", "science_type", "classes", "class_groups")

    def create(self, validated_data):
        user = self.context["request"].user
        instance = ChangeModerator.objects.create(**validated_data, user=user)
        return instance

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["science"] = ScienceSerializer(instance.science).data
        data["science_type"] = ScienceTypesSerializer(
            instance.science_type
        ).data
        data["classes"] = ClassesSerializer(instance.classes).data
        data["class_groups"] = ClassGroupSerializer(instance.class_groups).data
        return data
