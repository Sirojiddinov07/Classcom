from rest_framework import serializers
from core.apps.classcom import models, serializers as core_serializers


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Topic
        fields = "__all__"


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
    resources = core_serializers.ResourceSerializer(many=True)

    class Meta:
        model = models.Topic
        fields = (
            "id",
            "name",
            "sequence_number",
            "resources",
        )
