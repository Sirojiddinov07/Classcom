from rest_framework import serializers
from .models import Orders


class OrderSerializer(serializers.ModelSerializer):

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
