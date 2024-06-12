from rest_framework import serializers

from core.apps.classcom import models
from core.apps.classcom.serializers import media


class PlanScienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Science
        fields = ("id", "name")


class PlanQuarterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Quarter
        fields = ("id", "name")


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


##############################################################################################################
# Plan Detail Serializer
##############################################################################################################
class PlanDetailSerializer(serializers.ModelSerializer):
    type = TypeSerializer()
    classes = PlanClassSerializer()
    topic = PlanTopicSerializer()
    quarter = PlanQuarterSerializer()
    science = PlanScienceSerializer()
    media = media.MediaSerializer(many=True, read_only=True)

    class Meta:
        model = models.Plan
        fields = (
            "id",
            "name",
            "description",
            "banner",
            "classes",
            "topic",
            "media",
            "type",
            "quarter",
            "science",
        )

class PlanSerializer(serializers.ModelSerializer):
    """
    <<<<<<< HEAD
        PlanSerializer class
        note:
            O'qituvchi uchun tematik plan
    =======
        PlanSerializer class for Teachers
    >>>>>>> origin/dev
    """

    class Meta:
        model = models.Plan
        fields = (
            "id",
            "name",
            "description",
            "banner",
            "classes",
            "topic",
            "media",
            "type",
            "quarter",
            "science",
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
            "hour",
            "media",
            "_media",
        )

    def create(self, validated_data):
        validated_data.pop("user", None)
        media = validated_data.pop("media", [])
        resource = models.Plan.objects.create(
            user=self.context["request"].user, **validated_data
        )
        for media_item in media:
            media = models.Media.objects.create(file=media_item)
            resource.plan_resource.add(media)
        return resource
