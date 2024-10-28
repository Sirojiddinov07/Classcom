from rest_framework import serializers

from core.apps.classcom.models import TMRAppeal


class TMRAppealSerializer(serializers.ModelSerializer):
    class Meta:
        model = TMRAppeal
        fields = (
            "id",
            "status",
            "science",
            "science_type",
            "classes",
            "class_groups",
            "created_at",
            "updated_at",
        )
        read_only_fields = ["status"]

    def to_representation(self, instance):
        context = super().to_representation(instance)
        context["status"] = instance.get_status_display()
        context["science"] = instance.science.name
        context["science_type"] = instance.science_type.name
        context["classes"] = instance.classes.name
        context["class_groups"] = instance.class_groups.name
        return context

    def create(self, validated_data):
        return TMRAppeal.objects.create(
            **validated_data, user=self.context["request"].user
        )
