from rest_framework import serializers
from core.apps.classcom import models


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Resource
        fields = "__all__"
