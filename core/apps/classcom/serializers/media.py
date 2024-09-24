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
        validated_data["user"] = user
        if validated_data.get("desc") is None:
            validated_data["desc"] = validated_data[
                "file"
            ].name + datetime.now().strftime("_%Y-%m-%d_%H-%M-%S")
        media = Media.objects.create(**validated_data)
        return media


class MediaDetailSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

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
        )

    def get_user(self, obj):
        from core.http.serializers import UserSerializer

        return UserSerializer(obj.user).data
