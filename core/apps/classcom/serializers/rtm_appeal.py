import logging

from rest_framework import serializers

from core.apps.classcom.models import PlanAppeal, TmrFiles
from core.apps.classcom.serializers import (
    ScienceSerializer,
    ScienceTypesSerializer,
    ClassesSerializer,
)
from core.http.serializers import ClassGroupSerializer


class TmrFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TmrFiles
        fields = "__all__"


class PlanAppealSerializer(serializers.ModelSerializer):
    docs = serializers.ListField(
        child=serializers.FileField(), write_only=True
    )

    class Meta:
        model = PlanAppeal
        fields = (
            "id",
            "science",
            "science_type",
            "classes",
            "class_groups",
            "status",
            "docs",
        )

    def create(self, validated_data):
        try:
            user = self.context["request"].user
            docs = validated_data.pop("docs")

            instance = PlanAppeal.objects.create(**validated_data, user=user)
            for doc in docs:
                instance.docs.create(file=doc)
            return instance
        except Exception as e:
            logging.error(f"Error in create method: {str(e)}")
            raise serializers.ValidationError({"detail": str(e)})

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["science"] = ScienceSerializer(instance.science).data
        data["science_type"] = ScienceTypesSerializer(
            instance.science_type
        ).data
        data["classes"] = ClassesSerializer(instance.classes).data
        data["class_groups"] = ClassGroupSerializer(instance.class_groups).data
        data["docs"] = TmrFilesSerializer(instance.docs.all(), many=True).data
        return data
