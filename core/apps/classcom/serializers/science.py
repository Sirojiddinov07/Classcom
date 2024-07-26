from rest_framework import serializers

from core.apps.classcom.models import Science


class ScienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Science
        fields = ["id", "name", "science_grp", "created_at"]


class ScienceMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Science
        fields = ("id", "name")
