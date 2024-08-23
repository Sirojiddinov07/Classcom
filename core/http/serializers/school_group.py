from rest_framework import serializers

from core.http.models import ClassGroup


class ClassGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassGroup
        fields = ["id", "name"]
        read_only_fields = ["id"]
        extra_kwargs = {
            "name": {"required": True},
        }
