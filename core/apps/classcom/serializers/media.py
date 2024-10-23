from datetime import datetime

from rest_framework import serializers

from core.apps.classcom.models import Media


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = (
            "id",
            "desc",
            "file",
        )

    def create(self, validated_data):
        user = self.context["request"].user
        topic_id = self.context["request"].query_params.get("topic_id")
        validated_data["user"] = user
        if validated_data.get("desc") is None:
            validated_data["desc"] = validated_data[
                "file"
            ].name + datetime.now().strftime("_%Y-%m-%d_%H-%M-%S")
        media = Media.objects.create(
            **validated_data, object_type="plan", object_id=topic_id
        )
        return media


class MediaDetailSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    is_author = serializers.SerializerMethodField()

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
            "created_at",
            "user",
            "is_author",
        )

    def get_user(self, obj):
        from core.http.serializers import UserSerializer

        return UserSerializer(obj.user).data

    def get_is_author(self, obj):
        request = self.context.get("request", None)
        if request is None:
            return False
        return obj.user == request.user


class MediaMiniSerializer(serializers.ModelSerializer):
    is_author = serializers.SerializerMethodField()

    class Meta:
        model = Media
        fields = (
            "id",
            "user",
            "name",
            "desc",
            "type",
            "size",
            "is_author",
            "created_at",
        )

    def get_is_author(self, obj):
        return obj.user == self.context["request"].user
