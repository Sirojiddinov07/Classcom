from rest_framework import serializers
from .models import Orders


class OrderSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
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


class PaymentCreateSerializer(serializers.Serializer):
    order = serializers.PrimaryKeyRelatedField(queryset=Orders.objects.all())
