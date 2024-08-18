from rest_framework import serializers

from core.apps.classcom import models


class ClassTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ClassType
        fields = ["id", "name"]


class ClassesSerializer(serializers.ModelSerializer):
    type = ClassTypeSerializer(required=False)

    class Meta:
        model = models.Classes
        fields = ["id", "name", "type"]


class ClassMiniSerializer(serializers.ModelSerializer):
    type = ClassTypeSerializer(required=False)

    class Meta:
        model = models.Classes
        fields = ("id", "name", "type")
