from rest_framework import serializers
from .models import Orders
from ..classcom.serializers import ScienceTypesSerializer


class OrderSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        # instance.types = ScienceTypesSerializer(instance.types.all(), many=True).data
        return super().to_representation(instance)

    class Meta:
        fields = (
            "id",
            "start_date",
            "end_date",
            "science",
            "types",
            "price",
            "status",
        )
        model = Orders
        extra_kwargs = {
            "start_date": {
                "read_only": True
            },
            "end_date": {
                "read_only": True
            },
            "price": {
                "read_only": True
            },
            "status": {
                "read_only": True
            }
        }
