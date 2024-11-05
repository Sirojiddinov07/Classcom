from rest_framework import serializers

from core.apps.classcom.models.chat import Chat


class ChatSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
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
            "is_read",
        ]

    def get_user(self, obj):
        from core.http.serializers import UserSerializer

        return UserSerializer(obj.user).data

    def get_responsed(self, obj):
        return obj.response is not None
