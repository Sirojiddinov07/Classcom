from rest_framework import serializers

from core.apps.classcom import models
from core.apps.classcom.serializers.media import MediaDetailSerializer


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Topic
        fields = [
            "id",
            "name",
            "description",
            "hours",
            "sequence_number",
            "banner",
        ]

    def create(self, validated_data):
        topic = models.Topic.objects.create(**validated_data)
        return topic


class TopicDetailSerializer(serializers.ModelSerializer):
    media = MediaDetailSerializer(many=True)

    class Meta:
        model = models.Topic
        fields = [
            "id",
            "name",
            "description",
            "hours",
            "sequence_number",
            "created_at",
            "banner",
            "media_creatable",
            "media",
        ]
        extra_kwargs = {"media": {"required": False}}
