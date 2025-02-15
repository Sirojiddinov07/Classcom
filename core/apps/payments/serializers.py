from rest_framework import serializers

from core.apps.classcom.serializers import (
    ScienceTypesSerializer,
    ScienceMiniSerializer,
)
from .models import Orders


class OrderSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["types"] = ScienceTypesSerializer(
            instance=instance.types, many=True
        ).data
        data["science"] = ScienceMiniSerializer(instance=instance.science).data
        data["class_type"] = instance.class_type.name
        return data

    class Meta:
        fields = (
            "id",
            "start_date",
            "end_date",
            "science",
            "types",
            "class_type",
            "price",
            "status",
        )
        model = Orders
        extra_kwargs = {
            "start_date": {"read_only": True},
            "end_date": {"read_only": True},
            "price": {"read_only": True},
            "status": {"read_only": True},
        }


class PaymentCreateSerializer(serializers.Serializer):
    order = serializers.PrimaryKeyRelatedField(queryset=Orders.objects.all())
    status = serializers.BooleanField(read_only=True)


class UzumWebhookSerializer(serializers.Serializer):
    orderId = serializers.CharField()
    bindingId = serializers.CharField()
    orderNumber = serializers.CharField()
    operationType = serializers.CharField()
    operationState = serializers.CharField()
