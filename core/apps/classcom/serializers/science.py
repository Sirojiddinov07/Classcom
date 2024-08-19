from rest_framework import serializers

from core.apps.classcom.models import Science, ScienceTypes


class ScienceTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScienceTypes
        fields = ("id", "name")


class ScienceSerializer(serializers.ModelSerializer):
    types = ScienceTypesSerializer(many=True)

    class Meta:
        model = Science
        fields = ["id", "name", "science_grp", "types", "created_at"]


class ScienceMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Science
        fields = ("id", "name")
