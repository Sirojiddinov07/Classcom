from rest_framework import serializers

from core.apps.classcom import models
from core.apps.classcom.serializers import media
from core.apps.classcom.serializers.resource_type import ResourceTypeSerializer
from core.http import serializers as http_serializers

from .topic import TopicMiniSerializer


class ClassesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Classes
        fields = ("id", "name",)


class ResourceSerializer(serializers.ModelSerializer):
    """
    Serializer for the Resource model
    """

    user = http_serializers.UserSerializer()
    media = media.MediaSerializer(many=True, read_only=True)
    topic = TopicMiniSerializer(read_only=True)
    type = ResourceTypeSerializer(read_only=True)
    classes = ClassesSerializer(read_only=True)

    class Meta:
        model = models.Resource
        fields = (
            "id",
            "name",
            "classes",
            "topic",
            "media",
            "type",
            "user",
        )
        extra_kwargs = {"media": {"write_only": True}}


class ResourceDetailSerializer(ResourceSerializer):
    """
    Serializer for resource detail page
    """

    class Meta:
        model = models.Resource
        fields = ResourceSerializer.Meta.fields + (
            "banner",
            "description",
            "user",
        )
        extra_kwargs = ResourceSerializer.Meta.extra_kwargs


class ResourceCreateSerializer(serializers.ModelSerializer):
    media_file = serializers.FileField(write_only=True)
    _media = serializers.SerializerMethodField(read_only=True)

    def get__media(self, obj):
        return media.MediaSerializer(obj.media.first()).data

    class Meta:
        model = models.Resource
        fields = (
            "name",
            "description",
            "banner",
            "type",
            "topic",
            "classes",
            "media_file",
            "_media",
        )

    def create(self, validated_data):
        media_file = validated_data.pop("media_file")
        validated_data.pop("user", None)
        resource = models.Resource.objects.create(
            user=self.context["request"].user, **validated_data
        )

        resource.media.create(
            file=media_file, name=media_file.name, size=media_file.size
        )

        return resource
