import logging

from rest_framework import serializers, exceptions
from rest_framework import status
from rest_framework.response import Response

from core.apps.classcom.models import (
    Science,
    ScienceTypes,
    Classes,
    TmrFiles,
    PlanAppeal,
)
from core.apps.classcom.models.changing import ChangeModerator, ClassGroup


class PlanAppealSerializer(serializers.ModelSerializer):
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
    tmr_files = serializers.ListField(
        child=serializers.FileField(), write_only=True
    )

    class Meta:
        model = PlanAppeal
        fields = ("id", "science", "science_type", "classes", "class_groups")

    def create(self, validated_data):
        try:
            request = self.context.get("request")
            user = self.context["request"].user
            sciences = validated_data.pop("science")
            science_types = validated_data.pop("science_type")
            classes = validated_data.pop("classes")
            class_groups = validated_data.pop("class_groups")

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

            instance = ChangeModerator.objects.create(
                **validated_data, user=user
            )
            instance.science.set(sciences)
            instance.science_type.set(science_types)
            instance.classes.set(classes)
            instance.class_groups.set(class_groups)
            for doc_data in docs_data:
                document = TmrFiles.objects.create(
                    file=doc_data["docs"], description=doc_data["description"]
                )
                instance.tmr_files.add(document)
            return instance
        except Exception as e:
            logging.error(f"Error in create method: {str(e)}")
            raise exceptions.ValidationError({"detail": str(e)})
