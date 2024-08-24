from rest_framework.serializers import ModelSerializer

from core.apps.classcom.models import ResourceType


class TypeSerializer(ModelSerializer):
    class Meta:
        model = ResourceType
        fields = ("id", "name")
