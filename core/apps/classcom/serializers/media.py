from rest_framework import serializers
from .science import ScienceMiniSerializer
from .classes import ClassMiniSerializer
from .topic import TopicMiniSerializer
from core.http.serializers import UserSerializer

from core.apps.classcom import models


class MediaSerializer(serializers.ModelSerializer):
    science = serializers.SerializerMethodField()
    topic = serializers.SerializerMethodField()
    _class = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    def get_science(self, obj):
        data = obj.resources.first()
        if data is not None:
            return ScienceMiniSerializer(data.topic.science).data
        return None

    def get_topic(self, obj):
        data = obj.resources.first()
        if data is not None:
            return TopicMiniSerializer(obj.resources.first().topic).data
        return None

    def get__class(self, obj):
        data = obj.resources.first()
        if data is not None:
            return ClassMiniSerializer(obj.resources.first().classes).data
        return None

    def get_user(self, obj):
        data = obj.resources.first()
        if data is not None:
            return UserSerializer(obj.resources.first().user).data
        return None

    class Meta:
        model = models.Media
        fields = (
            "id",
            "name",
            "desc",
            "file",
            "topic",
            "science",
            "_class",
            "user",
            "size",
            "created_at",
            "updated_at",
        )


class MediaMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Media
        fields = ("id", "name")
