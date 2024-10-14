import logging

from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response

from core.apps.classcom.models import ScienceTypes, PlanAppeal, TmrFiles
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
    science_type = serializers.ListField(
        child=serializers.PrimaryKeyRelatedField(
            queryset=ScienceTypes.objects.all()
        )
    )
    tmr_files = serializers.ListField(
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
            "tmr_files",
        )

    def create(self, validated_data):
        try:
            request = self.context.get("request")
            user = self.context["request"].user
            science_types = validated_data.pop("science_type")

            docs_data = []

            for key in request.data:
                if key.startswith("description[") and key.endswith("]"):
                    index = key[len("description[") : -1]  # noqa: E203
                    file_key = f"docs[{index}]"
                    doc_desc = request.data.get(key)
                    doc_file = request.FILES.get(file_key)

                    if not doc_file:
                        return Response(
                            {
                                "error": f"File is required for document item {index}"
                            },
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                    if not doc_desc:
                        doc_desc = doc_file.name
                    docs_data.append(
                        {"docs": doc_file, "description": doc_desc}
                    )

            instance = PlanAppeal.objects.create(**validated_data, user=user)
            instance.science_type.set(science_types)
            for doc_data in docs_data:
                document = TmrFiles.objects.create(
                    file=doc_data["docs"], description=doc_data["description"]
                )
                instance.tmr_files.add(document)
            return instance
        except Exception as e:
            logging.error(f"Error in create method: {str(e)}")
            raise serializers.ValidationError({"detail": str(e)})

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["science"] = ScienceSerializer(instance.science).data
        data["science_type"] = ScienceTypesSerializer(
            instance.science_type, many=True
        ).data
        data["classes"] = ClassesSerializer(instance.classes).data
        data["class_groups"] = ClassGroupSerializer(instance.class_groups).data
        data["tmr_files"] = TmrFilesSerializer(
            instance.tmr_files.all(), many=True
        ).data
        return data
