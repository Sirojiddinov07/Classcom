from rest_framework import serializers

from core.apps.classcom.serializers.district import DistrictSerializer
from core.http import models


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Region
        fields = ["id", "region"]
        ordering = ["region"]


class RegionDetailSerializer(serializers.ModelSerializer):
    districts = DistrictSerializer(many=True, read_only=True)

    class Meta:
        model = models.Region
        fields = ["id", "region", "districts"]
        ordering = ["districts"]
