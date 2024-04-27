from rest_framework import serializers

from core.apps.classcom import models


class PlanSerializer(serializers.ModelSerializer):
    """
    PlanSerializer class for Teachers
    """

    class Meta:
        model = models.Plan
        fields = "__all__"
