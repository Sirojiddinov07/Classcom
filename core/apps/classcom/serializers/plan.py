from rest_framework import serializers

from core.apps.classcom import (
    models,
    services,
    serializers as class_serializers,
)
from core.apps.classcom.serializers import media



class PlanScienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Science
        fields = ("id", "name")


class PlanQuarterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Quarter
        fields = ("id", "choices", "start_date", "end_date")


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ResourceType
        fields = ("id", "name")


class PlanClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Classes
        fields = ("id", "name")


class PlanTopicSerializer(serializers.ModelSerializer):
    quarter = PlanQuarterSerializer()
    science = PlanScienceSerializer()

    class Meta:
        model = models.Topic
        fields = ("id", "name", "quarter", "science")


class MediaSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Media
        fields = ("id", "name")


##############################################################################################################
# Plan Detail Serializer
##############################################################################################################
class PlanDetailSerializer(serializers.ModelSerializer):
    type = TypeSerializer()
    classes = PlanClassSerializer()
    topic = PlanTopicSerializer()
    quarter = PlanQuarterSerializer()
    science = PlanScienceSerializer()
    plan_resource = MediaSerializer(many=True, read_only=True)

    class Meta:
        model = models.Plan
        fields = (
            "id",
            "name",
            "description",
            "banner",
            "classes",
            "topic",
            "type",
            "quarter",
            "science",
            "plan_resource",
        )


class PlanSerializer(serializers.ModelSerializer):
    """
    PlanSerializer class
    note:
        O'qituvchi uchun tematik plan
    """

    status = serializers.SerializerMethodField()
    classes = PlanClassSerializer()
    quarter = PlanQuarterSerializer()
    science = PlanScienceSerializer()
    def get_status(self, obj):
        return "active"

    class Meta:
        model = models.Plan
        fields = (
            "id",
            # "name",
            # "description",
            # "banner",
            "classes",
            # "topic",
            # "type",
            "quarter",
            "science",
            "status",
        )


###########################################################
# Plan Create Serializer
###########################################################
class PlanCreateSerializer(serializers.ModelSerializer):
    _media = media.MediaSerializer(
        many=True, read_only=True, source="plan_resource"
    )
    media = serializers.ListField(
        child=serializers.FileField(), write_only=True
    )
    names = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
    )
    descriptions = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
    )
    _topic = class_serializers.TopicMiniSerializer(
        read_only=True, source="topic"
    )
    _class = class_serializers.ClassMiniSerializer(
        read_only=True, source="classes"
    )
    _quarter = class_serializers.QuarterMiniSerializer(
        read_only=True, source="quarter"
    )
    _science = class_serializers.ScienceMiniSerializer(
        read_only=True, source="science"
    )

    class Meta:
        model = models.Plan
        fields = (
            "name",
            "description",
            "banner",
            "type",
            "topic",
            "classes",
            "quarter",
            "science",
            "media",
            "names",
            "descriptions",
            "hour",
            "_topic",
            "_class",
            "_quarter",
            "_science",
            "_media",
        )
        extra_kwargs = {"classes": {"write_only": True}}

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return services.BaseService().serializer_name_replace(
            data,
            [
                "_topic",
                "_class",
                "_quarter",
                "_science",
                "_media",
            ],
        )

    def create(self, validated_data):
        validated_data.pop("user", None)
        media = validated_data.pop("media", [])
        names = validated_data.pop("names", [])
        descriptions = validated_data.pop("descriptions", [])
        service = services.BaseService()

        resource = models.Plan.objects.create(
            user=self.context["request"].user, **validated_data
        )
        for index, media_item in enumerate(media):
            media = models.Media.objects.create(
                file=media_item,
                name=service.list_index_default(names, index),
                desc=service.list_index_default(descriptions, index),
            )
            resource.plan_resource.add(media)
        return resource
