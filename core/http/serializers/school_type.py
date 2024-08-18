from rest_framework import serializers

from core.http.models import SchoolType


class SchoolTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolType
        fields = ["id", "name"]
        read_only_fields = ["id"]
        extra_kwargs = {
            "name": {"required": True},
        }
