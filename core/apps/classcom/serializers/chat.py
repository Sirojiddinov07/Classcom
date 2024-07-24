from rest_framework import serializers

from core.apps.classcom.models.chat import Chat
from core.http.serializers import UserSerializer


class ChatSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    responsed = serializers.SerializerMethodField()
    response = serializers.CharField(read_only=True)

    class Meta:
        model = Chat
        fields = [
            "id",
            "user",
            "massage",
            "time",
            "responsed",
            "response",
            "response_time",
        ]

    def get_responsed(self, obj):
        return obj.response is not None
