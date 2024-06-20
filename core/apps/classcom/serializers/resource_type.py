from rest_framework import serializers

from core.apps.classcom.models import ResourceType


class ResourceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceType
        fields = ("name",)
