from rest_framework import serializers

from core.apps.classcom.models import Weeks
from core.apps.classcom.serializers import QuarterMiniSerializer


class WeeksSerializer(serializers.ModelSerializer):
    quarter = QuarterMiniSerializer()

    class Meta:
        model = Weeks
        fields = [
            "id",
            "quarter",
            "week_count",
            "start_date",
            "end_date",
            "created_at",
        ]
