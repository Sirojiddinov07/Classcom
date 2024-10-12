from rest_framework import serializers

from core.apps.classcom.models import Science, ScienceTypes, Moderator


class ScienceTypesSerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField()

    class Meta:
        model = ScienceTypes
        fields = ("id", "name", "count")

    def get_count(self, obj):
        return Moderator.objects.filter(science_type=obj).count()


class ScienceSerializer(serializers.ModelSerializer):
    types = ScienceTypesSerializer(many=True)
    count = serializers.SerializerMethodField()

    class Meta:
        model = Science
        fields = [
            "id",
            "name",
            "science_grp",
            "types",
            "class_group",
            "created_at",
            "count",
        ]

    def get_count(self, obj):
        return Moderator.objects.filter(science=obj).count()


class ScienceMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Science
        fields = ("id", "name")
