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
            "weeks",
            "sequence_number",
            "banner",
        ]

    def create(self, validated_data):
        user = self.context["request"].user
        topic = models.Topic.objects.create(**validated_data, user=user)
        return topic


class TopicDetailSerializer(serializers.ModelSerializer):
    media = MediaDetailSerializer(many=True)
    user = serializers.SerializerMethodField()
    media_count = serializers.SerializerMethodField()
    download_count = serializers.SerializerMethodField()

    class Meta:
        model = models.Topic
        fields = [
            "id",
            "name",
            "description",
            "hours",
            "sequence_number",
            "created_at",
            "media_creatable",
            "weeks",
            "media",
            "banner",
            "user",
            "view_count",
            "media_count",
            "download_count",
        ]
        extra_kwargs = {"media": {"required": False}}

    def get_user(self, obj):
        from core.http.serializers.user import UserSerializer

        return UserSerializer(obj.user).data

    def get_media_count(self, obj):
        return obj.media_count

    def get_download_count(self, obj):
        return obj.all_download_count
