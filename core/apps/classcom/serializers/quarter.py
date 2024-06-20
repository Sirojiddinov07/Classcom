from rest_framework import serializers
from core.apps.classcom import models


class QuarterMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Quarter
        fields = ("id", "choices", "start_date", "end_date")
