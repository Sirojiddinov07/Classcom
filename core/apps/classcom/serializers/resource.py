from rest_framework import serializers
from rest_framework.exceptions import APIException

from core.apps.classcom import models
from core.apps.classcom.serializers import (
    CategorySerializer,
    CategoryTypeSerializer,
)
from core.apps.classcom.serializers import media
from core.apps.classcom.serializers.resource_type import (
    ResourceTypeMiniSerializer,
)
from core.http import serializers as http_serializers
from ..choices import Types, Departments, Schools, Docs


class ClassesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Classes
        fields = ("id", "name")


class ResourceSerializer(serializers.ModelSerializer):
    user = http_serializers.UserSerializer()
    media = media.MediaSerializer(many=True, read_only=True)
    type = ResourceTypeMiniSerializer(read_only=True)
    classes = ClassesSerializer(read_only=True)
    subtype = serializers.SerializerMethodField()
    category = CategorySerializer()
    category_type = CategoryTypeSerializer()

    def get_subtype(self, obj):
        try:
            match obj.type.type:
                case Types.BYCLASS | Types.BYCLASSANDUNIT:
                    return ClassesSerializer(
                        models.Classes.objects.get(id=obj.subtype)
                    ).data
                case Types.BYDEPARTMENT:
                    data = Departments(obj.subtype)
                    return {"id": data.name, "name": data.label}
                case Types.BYSCHOOL:
                    data = Schools(obj.subtype)
                    return {"id": data.name, "name": data.label}
                case Types.BYDOCS:
                    data = Docs(obj.subtype)
                    return {"id": data.name, "name": data.label}
                case _:
                    return None
        except Exception as e:
            raise APIException(e)

    class Meta:
        model = models.Resource
        fields = (
            "id",
            "name",
            "category",
            "classes",
            "media",
            "type",
            "subtype",
            "category_type",
            "source",
            "degree",
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
        data["type"] = ResourceTypeMiniSerializer(instance.type).data
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
            "source",
            "degree",
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
