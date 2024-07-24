from rest_framework import serializers

from core.http import models


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.District
        fields = ["id", "district"]
