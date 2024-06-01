from core.http import serializers
from core.http.choices import Region


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ["id", "region"]