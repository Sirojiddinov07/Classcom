from rest_framework import serializers

from core.apps.classcom.models import Science


class ScienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Science
        fields = "__all__"


class ScienceMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Science
        fields = ("id", "name")
