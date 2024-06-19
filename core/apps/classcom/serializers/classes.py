from rest_framework import serializers
from core.apps.classcom import models


class ClassesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Classes
        fields = "__all__"


class ClassMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Classes
        fields = ("id", "name")
