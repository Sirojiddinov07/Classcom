from rest_framework import serializers

from core.apps.classcom import models
from .classes import ClassMiniSerializer
from .quarter import QuarterMiniSerializer
from .science import ScienceMiniSerializer


class TopicSerializer(serializers.ModelSerializer):
    _class = ClassMiniSerializer(read_only=True)
    quarter = QuarterMiniSerializer(read_only=True)
    science = ScienceMiniSerializer(read_only=True)

    class Meta:
        model = models.Topic
        fields = [
            "id",
            "name",
            "_class",
            "quarter",
            "science",
            "sequence_number",
            "thematic_plan",
        ]


class TopicMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Topic
        fields = ("id", "name")


class TopicFilterSerializer(serializers.ModelSerializer):
    date = serializers.DateField(required=False, format="%d.%m.%Y")

    class Meta:
        model = models.Topic
        fields = ("_class", "science", "date")


class TopicCalculationSerializer(serializers.ModelSerializer):
    resources = serializers.SerializerMethodField()

    class Meta:
        model = models.Topic
        fields = (
            "id",
            "name",
            "sequence_number",
            "resources",
        )

    def get_resources(self, obj):
        from .resource import ResourceSerializer  # Lazy import here

        return ResourceSerializer(obj.resources.all(), many=True).data
