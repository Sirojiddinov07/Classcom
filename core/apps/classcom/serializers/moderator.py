from rest_framework import serializers

from core.apps.classcom import models


class ModeratorSerializer(serializers.ModelSerializer):
    docs = serializers.SerializerMethodField()

    class Meta:
        model = models.Moderator
        fields = (
            "id",
            "user",
            "balance",
            "science",
            "classes",
            "degree",
            "docs",
            "is_contracted",
        )

    def get_docs(self, obj):
        if obj.docs:
            return obj.docs.url
        return None
