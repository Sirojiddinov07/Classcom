from rest_framework import serializers

from core.apps.classcom.models import Download, Resource, Topic, Media
from core.apps.classcom.serializers import (
    MobileTopicDetailSerializer,
    MediaMiniSerializer,
)
from core.apps.classcom.serializers.resource import ResourceDetailSerializer


class DownloadHistorySerializer(serializers.ModelSerializer):
    data = serializers.SerializerMethodField()
    media = MediaMiniSerializer()

    class Meta:
        model = Download
        fields = (
            "id",
            "date",
            "media",
            "object_type",
            "object_id",
            "user",
            "data",
        )

    def get_data(self, instance):
        if instance.object_type == "plan":
            try:
                topic = Topic.objects.get(id=instance.object_id)
                return MobileTopicDetailSerializer(topic).data
            except Topic.DoesNotExist:
                return {}
        elif instance.object_type == "resource":
            try:
                resource = Resource.objects.get(id=instance.object_id)
                return ResourceDetailSerializer(resource).data
            except Resource.DoesNotExist:
                return {}
        return {}

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["data"] = self.get_data(instance)
        return data


class UploadMediaSerializer(serializers.ModelSerializer):
    data = serializers.SerializerMethodField()

    class Meta:
        model = Media
        fields = (
            "id",
            "name",
            "desc",
            "type",
            "size",
            "count",
            "statistics",
            "object_type",
            "object_id",
            "created_at",
            "user",
            "data",
        )

    def get_data(self, instance):
        if instance.object_type == "plan":
            try:
                topic = Topic.objects.get(id=instance.object_id)
                return MobileTopicDetailSerializer(topic).data
            except Topic.DoesNotExist:
                return {}
        elif instance.object_type == "resource":
            try:
                resource = Resource.objects.get(id=instance.object_id)
                return ResourceDetailSerializer(resource).data
            except Resource.DoesNotExist:
                return {}
        return {}

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["data"] = self.get_data(instance)
        return data
