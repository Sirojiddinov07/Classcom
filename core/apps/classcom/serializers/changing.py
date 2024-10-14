from rest_framework import serializers

from core.apps.classcom.models import ScienceTypes, ChangeModerator
from core.apps.classcom.serializers import (
    ScienceSerializer,
    ScienceTypesSerializer,
    ClassesSerializer,
)
from core.http.serializers import ClassGroupSerializer


class ChangeModeratorSerializer(serializers.ModelSerializer):
    science_type = serializers.ListField(
        child=serializers.PrimaryKeyRelatedField(
            queryset=ScienceTypes.objects.all()
        )
    )

    class Meta:
        model = ChangeModerator
        fields = ("id", "science", "science_type", "classes", "class_groups")

    def create(self, validated_data):
        user = self.context["request"].user
        science_types = validated_data.pop("science_type")

        instance = ChangeModerator.objects.create(**validated_data, user=user)
        instance.science_type.set(science_types)
        return instance

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["science"] = ScienceSerializer(instance.science).data
        data["science_type"] = ScienceTypesSerializer(
            instance.science_type, many=True
        ).data
        data["classes"] = ClassesSerializer(instance.classes).data
        data["class_groups"] = ClassGroupSerializer(instance.class_groups).data
        return data
