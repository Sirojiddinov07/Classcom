from rest_framework import serializers
from rest_framework.exceptions import APIException

from core.apps.classcom import models
from core.apps.classcom.models import Moderator
from core.apps.classcom.serializers import (
    CategorySerializer,
    CategoryTypeSerializer,
    ScienceSerializer,
)
from core.apps.classcom.serializers import media
from core.apps.classcom.serializers.resource_type import (
    ResourceTypeMiniSerializer,
)
from ..choices import Types, Departments, Schools, Docs


class ClassesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Classes
        fields = ("id", "name")


class ResourceSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    media = media.MediaDetailSerializer(many=True, read_only=True)
    type = ResourceTypeMiniSerializer(read_only=True)
    classes = ClassesSerializer(read_only=True)
    subtype = serializers.SerializerMethodField()
    category = CategorySerializer()
    category_type = CategoryTypeSerializer()
    science = ScienceSerializer(read_only=True)

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
                case Types.BYSCIENCE:
                    return ScienceSerializer(
                        models.Science.objects.get(id=obj.subtype)
                    ).data
                case _:
                    return None
        except Exception as e:
            raise APIException(e)

    def get_user(self, obj):
        from core.http.serializers import UserSerializer

        return UserSerializer(obj.user).data

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get("request")
        if request:
            lang = request.headers.get("Accept-Language", "ru")
            if lang == "uz":
                data["name"] = (
                    instance.name_uz or instance.name or instance.name_ru
                )
            elif lang == "ru":
                data["name"] = (
                    instance.name_ru or instance.name or instance.name_uz
                )
            else:
                data["name"] = (
                    instance.name or instance.name_uz or instance.name_ru
                )
        return data

    class Meta:
        model = models.Resource
        fields = (
            "id",
            "name",
            "category",
            "classes",
            "science",
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
    media_files = serializers.ListField(
        child=serializers.FileField(), write_only=True
    )
    _media = serializers.SerializerMethodField(read_only=True)

    def get__media(self, obj):
        return media.MediaDetailSerializer(obj.media.first()).data

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["type"] = ResourceTypeMiniSerializer(instance.type).data
        return data

    class Meta:
        model = models.Resource
        fields = (
            "id",
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
            "science",
            "media_files",
            "_media",
        )
        extra_kwargs = {"type": {"required": True}}

    def create(self, validated_data):
        user = self.context["request"].user
        try:
            moderator = Moderator.objects.get(user=user)
            if not moderator.resource_creatable:
                raise APIException("User is not allowed to create resources.")
        except Moderator.DoesNotExist:
            raise APIException("User is not a moderator.")

        media_files = validated_data.pop("media_files")
        validated_data.pop("user", None)
        resource = models.Resource.objects.create(user=user, **validated_data)

        for media_file in media_files:
            resource.media.create(
                file=media_file,
                name=media_file.name,
                size=media_file.size,
                user=user,
                object_type="resource",
                object_id=resource.id,
            )

        return resource
