from rest_framework import serializers

from core.apps.classcom.models import Ai


class AiSerializer(serializers.ModelSerializer):
    is_author = serializers.SerializerMethodField()

    class Meta:
        model = Ai
        fields = (
            "id",
            "topic",
            "user",
            "question",
            "answer",
            "is_author",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")

    def get_is_author(self, obj):
        return self.context["request"].user == obj.user
