from core.http import serializers
from core.http.choices import District


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ["id", "district", "region"]