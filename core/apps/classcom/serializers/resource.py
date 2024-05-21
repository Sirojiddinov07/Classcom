from rest_framework import serializers

from core.apps.classcom import models
from core.apps.classcom.serializers import media


class ResourceSerializer(serializers.ModelSerializer):
    """
    Serializer for the Resource model
    """

    media = media.MediaSerializer(many=True, read_only=True)

    class Meta:
        model = models.Resource
        fields = (
            "id", "name",
            "classes", "topic", "media"
        )
        extra_kwargs = {"media": {"write_only": True}}


class ResourceDetailSerializer(ResourceSerializer):
    """
    Serializer for resource detail page
    """

    class Meta:
        model = models.Resource
        fields = ResourceSerializer.Meta.fields + ("media",)
        extra_kwargs = ResourceSerializer.Meta.extra_kwargs
