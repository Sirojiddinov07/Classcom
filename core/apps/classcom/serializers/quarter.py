from rest_framework import serializers

from core.apps.classcom.models import Quarter


class QuarterMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quarter
        fields = ("id", "choices", "start_date", "end_date")
