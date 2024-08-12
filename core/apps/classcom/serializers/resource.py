from rest_framework import serializers
from core.apps.classcom import models
from core.apps.classcom.serializers import media
from core.apps.classcom.serializers import (
    CategorySerializer,
    CategoryTypeSerializer,
)
from core.apps.classcom.serializers.resource_type import ResourceTypeMiniSerializer
from core.http import serializers as http_serializers


class ClassesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Classes
        fields = ("id", "name")


class ResourceSerializer(serializers.ModelSerializer):
    user = http_serializers.UserSerializer()
    media = media.MediaSerializer(many=True, read_only=True)
    type = ResourceTypeMiniSerializer(read_only=True)
    classes = ClassesSerializer(read_only=True)
    category = CategorySerializer()
    category_type = CategoryTypeSerializer()

    class Meta:
        model = models.Resource
        fields = (
            "id",
            "name",
            "category",
            "classes",
            "media",
            "type",
            "category_type",
            "user",
        )
        extra_kwargs = {"media": {"write_only": True}}


class ResourceDetailSerializer(ResourceSerializer):
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

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['type'] = ResourceTypeMiniSerializer(instance.type).data
        return data

    class Meta:
        model = models.Resource
        fields = (
            "name",
            "category",
            "category_type",
            "description",
            "banner",
            "type",
            "subtype",
            "classes",
            "media_file",
            "_media",
        )
        extra_kwargs = {"type": {"required": True}}

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
