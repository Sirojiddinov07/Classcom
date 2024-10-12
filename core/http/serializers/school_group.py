from rest_framework import serializers

from core.apps.classcom.models import Moderator
from core.http.models import ClassGroup


class ClassGroupSerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField()

    class Meta:
        model = ClassGroup
        fields = ["id", "name", "count"]
        read_only_fields = ["id"]
        extra_kwargs = {
            "name": {"required": True},
            "count": {"read_only": True},
        }

    def get_count(self, obj):
        return Moderator.objects.filter(class_groups=obj).count()
