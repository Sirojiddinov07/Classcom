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
