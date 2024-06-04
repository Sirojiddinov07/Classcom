from rest_framework import serializers


class NotificationSerializer(serializers.Serializer):
    user = serializers.CharField(read_only=True)
    message = serializers.TimeField()
