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
            "classes", "topic", "media", "type"
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


class ResourceCreateSerializer(serializers.ModelSerializer):
    media = media.MediaSerializer(many=True)

    class Meta:
        model = models.Resource
        fields = ('name', 'description', 'banner', 'type', 'topic', 'classes', 'media')

    def create(self, validated_data):
        media_data = validated_data.pop('media')
        resource = models.Resource.objects.create(user=self.context['request'].user, **validated_data)
        for media_item in media_data:
            models.Media.objects.create(resource=resource, **media_item)
        return resource
