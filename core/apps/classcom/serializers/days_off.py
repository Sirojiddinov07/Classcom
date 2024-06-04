from rest_framework import serializers
from core.apps.classcom.models import DaysOff


class DaysOffSerializer(serializers.ModelSerializer):
    class Meta:
        model = DaysOff
        fields = ("from_date", "to_date", "reason")

    def create(self, validated_data):
        user = self.context["request"].user
        return DaysOff.objects.create(user=user, **validated_data)
