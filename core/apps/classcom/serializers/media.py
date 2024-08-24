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
        media = Media.objects.create(**validated_data)
        return media


class MediaDetailSerializer(serializers.ModelSerializer):
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
        )
