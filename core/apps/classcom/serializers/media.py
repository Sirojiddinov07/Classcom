from rest_framework import serializers

from core.apps.classcom import models
from ..models import Plan, Media


class MediaSerializer(serializers.ModelSerializer):
    science = serializers.SerializerMethodField()
    topic = serializers.SerializerMethodField()
    _class = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    class Meta:
        model = Media
        fields = (
            "id",
            "name",
            "desc",
            "file",
            "topic",
            "science",
            "_class",
            "user",
            "size",
            "created_at",
            "updated_at",
        )

    def get_science(self, obj):
        plan = Plan.objects.filter(plan_resource=obj).first()
        return plan.science.name if plan and plan.science else None

    def get_topic(self, obj):
        plan = Plan.objects.filter(plan_resource=obj).first()
        return plan.topic.name if plan and plan.topic else None

    def get__class(self, obj):
        plan = Plan.objects.filter(plan_resource=obj).first()
        return plan.classes.name if plan and plan.classes else None

    def get_user(self, obj):
        plan = Plan.objects.filter(plan_resource=obj).first()
        user = plan.user if plan else None
        return (
            {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
            }
            if user
            else None
        )


class MediaMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Media
        fields = ("id", "name")
