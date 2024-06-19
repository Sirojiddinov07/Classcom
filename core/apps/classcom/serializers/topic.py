from rest_framework import serializers
from core.apps.classcom import models


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Topic
        fields = "__all__"


class TopicMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Topic
        fields = ("id", "name")
