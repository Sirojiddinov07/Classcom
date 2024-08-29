from datetime import datetime

from rest_framework import serializers

from core.apps.classcom.models import Media
from core.http.serializers import UserSerializer


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
    user = UserSerializer()

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
