from rest_framework import serializers

from core.apps.classcom import models
from core.apps.classcom.models import Moderator


class ClassTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ClassType
        fields = ["id", "name"]


class ClassesSerializer(serializers.ModelSerializer):
    type = ClassTypeSerializer(required=False)
    count = serializers.SerializerMethodField()

    class Meta:
        model = models.Classes
        fields = ["id", "name", "type", "count"]

    def get_count(self, obj):
        return Moderator.objects.filter(classes=obj).count()


class ClassMiniSerializer(serializers.ModelSerializer):
    type = ClassTypeSerializer(required=False)

    class Meta:
        model = models.Classes
        fields = ("id", "name", "type")
