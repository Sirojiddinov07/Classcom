from django.conf import settings  # noqa
from django.conf import settings  # noqa
from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response

from core.apps.classcom.choices import Role
from core.apps.classcom.models import Moderator, Document
from core.apps.classcom.serializers import (
    DocumentSerializer,
    ScienceSerializer,
    ClassesSerializer,
    ScienceTypesSerializer,
)
from core.http import models
from core.http.serializers import SchoolTypeSerializer, ClassGroupSerializer


class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(max_length=None)
    school_type = SchoolTypeSerializer()
    resource_creatable = serializers.SerializerMethodField(read_only=True)
    plan_creatable = serializers.SerializerMethodField(read_only=True)
    topic_creatable = serializers.SerializerMethodField(read_only=True)
    is_contracted = serializers.SerializerMethodField(read_only=True)
    document = DocumentSerializer(many=True)

    class Meta:
        fields = [
            "id",
            "avatar",
            "first_name",
            "last_name",
            "father_name",
            "phone",
            "role",
            "region",
            "district",
            "science_group",
            "science",
            "classes",
            "school_type",
            "class_group",
            "institution",
            "institution_number",
            "document",
            "response_file",
            "resource_creatable",
            "plan_creatable",
            "topic_creatable",
            "is_contracted",
        ]
        extra_kwargs = {
            "role": {"read_only": True},
            "resource_creatable": {"read_only": True},
            "plan_creatable": {"read_only": True},
        }
        model = models.User

    def get_avatar(self, obj):
        if obj.avatar:
            return obj.avatar.url.replace(settings.MEDIA_URL, "/media/")
        return None

    def is_moderator(self, obj):
        return obj.role == Role.MODERATOR

    def get_is_contracted(self, obj):
        if self.is_moderator(obj):
            try:
                moderator = Moderator.objects.get(user=obj)
                return moderator.is_contracted
            except Moderator.DoesNotExist:
                return False
        return False

    def get_resource_creatable(self, obj):
        if self.is_moderator(obj):
            try:
                moderator = Moderator.objects.get(user=obj)
                return moderator.resource_creatable
            except Moderator.DoesNotExist:
                return False
        return False

    def get_plan_creatable(self, obj):
        if self.is_moderator(obj):
            try:
                moderator = Moderator.objects.get(user=obj)
                return moderator.plan_creatable
            except Moderator.DoesNotExist:
                return False
        return False

    def get_topic_creatable(self, obj):
        if self.is_moderator(obj):
            try:
                moderator = Moderator.objects.get(user=obj)
                return moderator.topic_creatable
            except Moderator.DoesNotExist:
                return False
        return False

    def update(self, instance, validated_data):
        request = self.context.get("request")
        docs_data = []
        print(validated_data)  # Debug line
        instance.avatar = validated_data.get("avatar", instance.avatar)
        instance.first_name = validated_data.get(
            "first_name", instance.first_name
        )
        instance.last_name = validated_data.get(
            "last_name", instance.last_name
        )
        instance.father_name = validated_data.get(
            "father_name", instance.father_name
        )
        instance.region = validated_data.get("region", instance.region)
        instance.district = validated_data.get("district", instance.district)
        instance.science_group = validated_data.get(
            "science_group", instance.science_group
        )
        instance.science = validated_data.get("science", instance.science)
        instance.classes = validated_data.get("classes", instance.classes)

        for key in request.data:
            if key.startswith("description[") and key.endswith("]"):
                index = key[len("description[") : -1]  # noqa: E203
                file_key = f"docs[{index}]"
                doc_desc = request.data.get(key)
                doc_file = request.FILES.get(file_key)

                if not doc_file:
                    return Response(
                        {
                            "error": f"File is required for document item {index}"
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                if not doc_desc:
                    doc_desc = doc_file.name
                docs_data.append({"docs": doc_file, "description": doc_desc})

        for doc_data in docs_data:
            document = Document.objects.create(
                file=doc_data["docs"], description=doc_data["description"]
            )
            instance.document.add(document)

        instance.save()
        return instance

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get("request")

        if request and request.user.role == Role.USER:
            data.pop("is_contracted", None)

        if request and request.headers:
            language = request.headers.get("Accept-Language", "uz")
        else:
            language = "uz"

        if language == "uz":
            data["default_document"] = (
                instance.default_document_uz.url
                if instance.default_document_uz
                else None
            )
        elif language == "ru":
            data["default_document"] = (
                instance.default_document_ru.url
                if instance.default_document_ru
                else None
            )

        return data


class UserRoleChangeSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=Role)

    class Meta:
        model = models.User
        fields = ["role"]


class UserDetailSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(max_length=None)
    school_type = SchoolTypeSerializer()
    science = ScienceSerializer()
    classes = ClassesSerializer()
    class_group = ClassGroupSerializer()
    science_group = ScienceTypesSerializer(many=True)
    resource_creatable = serializers.SerializerMethodField(read_only=True)
    plan_creatable = serializers.SerializerMethodField(read_only=True)
    topic_creatable = serializers.SerializerMethodField(read_only=True)
    is_contracted = serializers.SerializerMethodField(read_only=True)
    document = DocumentSerializer(many=True)

    class Meta:
        fields = [
            "id",
            "avatar",
            "first_name",
            "last_name",
            "father_name",
            "phone",
            "role",
            "region",
            "district",
            "science_group",
            "science",
            "classes",
            "school_type",
            "class_group",
            "institution",
            "institution_number",
            "document",
            "response_file",
            "resource_creatable",
            "plan_creatable",
            "topic_creatable",
            "is_contracted",
        ]
        extra_kwargs = {
            "role": {"read_only": True},
            "resource_creatable": {"read_only": True},
            "plan_creatable": {"read_only": True},
        }
        model = models.User

    def get_avatar(self, obj):
        if obj.avatar:
            return obj.avatar.url.replace(settings.MEDIA_URL, "/media/")
        return None

    def is_moderator(self, obj):
        return obj.role == Role.MODERATOR

    def get_is_contracted(self, obj):
        if self.is_moderator(obj):
            try:
                moderator = Moderator.objects.get(user=obj)
                return moderator.is_contracted
            except Moderator.DoesNotExist:
                return False
        return False

    def get_resource_creatable(self, obj):
        if self.is_moderator(obj):
            try:
                moderator = Moderator.objects.get(user=obj)
                return moderator.resource_creatable
            except Moderator.DoesNotExist:
                return False
        return False

    def get_plan_creatable(self, obj):
        if self.is_moderator(obj):
            try:
                moderator = Moderator.objects.get(user=obj)
                return moderator.plan_creatable
            except Moderator.DoesNotExist:
                return False
        return False

    def get_topic_creatable(self, obj):
        if self.is_moderator(obj):
            try:
                moderator = Moderator.objects.get(user=obj)
                return moderator.topic_creatable
            except Moderator.DoesNotExist:
                return False
        return False

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get("request")

        if request and request.user.role == Role.USER:
            data.pop("is_contracted", None)

        if request and request.headers:
            language = request.headers.get("Accept-Language", "uz")
        else:
            language = "uz"

        if language == "uz":
            data["default_document"] = (
                instance.default_document_uz.url
                if instance.default_document_uz
                else None
            )
        elif language == "ru":
            data["default_document"] = (
                instance.default_document_ru.url
                if instance.default_document_ru
                else None
            )

        return data
