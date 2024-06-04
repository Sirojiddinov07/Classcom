from rest_framework import serializers

from core.apps.classcom import models


class PlanSerializer(serializers.ModelSerializer):
    """
    <<<<<<< HEAD
        PlanSerializer class
        note:
            O'qituvchi uchun tematik plan
    =======
        PlanSerializer class for Teachers
    >>>>>>> origin/dev
    """

    class Meta:
        model = models.Plan
        fields = "__all__"
