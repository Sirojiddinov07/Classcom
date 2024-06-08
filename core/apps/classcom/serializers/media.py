from rest_framework import serializers

from core.apps.classcom import models


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Media
        fields = (
            "id",
            "name",
            "file",
            "size",
            "created_at",
            "updated_at",
        )

    def create(self, validated_data):
        file = validated_data.get("file")
        validated_data["type"] = file.content_type
        return super().create(validated_data)
