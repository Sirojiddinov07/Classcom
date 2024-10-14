from rest_framework import serializers

from core.apps.classcom.models import Science, ScienceTypes, Classes
from core.apps.classcom.models.changing import ChangeModerator, ClassGroup
from core.apps.classcom.serializers import (
    ScienceSerializer,
    ScienceTypesSerializer,
    ClassesSerializer,
)
from core.http.serializers import ClassGroupSerializer


class ChangeModeratorSerializer(serializers.ModelSerializer):
    science = serializers.PrimaryKeyRelatedField(
        queryset=Science.objects.all(), many=True
    )
    science_type = serializers.PrimaryKeyRelatedField(
        queryset=ScienceTypes.objects.all(), many=True
    )
    classes = serializers.PrimaryKeyRelatedField(
        queryset=Classes.objects.all(), many=True
    )
    class_groups = serializers.PrimaryKeyRelatedField(
        queryset=ClassGroup.objects.all(), many=True
    )

    class Meta:
        model = ChangeModerator
        fields = ("id", "science", "science_type", "classes", "class_groups")

    def create(self, validated_data):
        user = self.context["request"].user
        sciences = validated_data.pop("science")
        science_types = validated_data.pop("science_type")
        classes = validated_data.pop("classes")
        class_groups = validated_data.pop("class_groups")

        instance = ChangeModerator.objects.create(**validated_data, user=user)
        instance.science.set(sciences)
        instance.science_type.set(science_types)
        instance.classes.set(classes)
        instance.class_groups.set(class_groups)
        return instance

    def to_representation(self, instance):
        return {
            "id": instance.id,
            "science": ScienceSerializer(
                instance.science.all(), many=True
            ).data,
            "science_type": ScienceTypesSerializer(
                instance.science_type.all(), many=True
            ).data,
            "classes": ClassesSerializer(
                instance.classes.all(), many=True
            ).data,
            "class_groups": ClassGroupSerializer(
                instance.class_groups.all(), many=True
            ).data,
        }
