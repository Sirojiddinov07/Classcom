from rest_framework import serializers

from core.apps.classcom.models import Plan, Topic
from core.apps.classcom.serializers.classes import ClassesSerializer
from core.apps.classcom.serializers.quarter import QuarterMiniSerializer
from core.apps.classcom.serializers.science import ScienceSerializer
from core.apps.classcom.serializers.science import ScienceTypesSerializer
from core.http.serializers import ClassGroupSerializer


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = [
            "id",
            "language",
            "classes",
            "quarter",
            "science",
            "class_group",
            "science_types",
        ]
        extra_kwargs = {"id": {"read_only": True}}
        unique_together = (
            "classes",
            "quarter",
            "science",
            "class_group",
            "science_types",
        )

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["user"] = user

        plan = Plan.objects.create(**validated_data)
        return plan


class PlanDetailSerializer(serializers.ModelSerializer):
    classes = ClassesSerializer()
    user = serializers.SerializerMethodField()
    quarter = QuarterMiniSerializer()
    science = ScienceSerializer()
    class_group = ClassGroupSerializer()
    science_types = ScienceTypesSerializer()
    is_author = serializers.SerializerMethodField()
    is_topic = serializers.SerializerMethodField()

    class Meta:
        model = Plan
        fields = [
            "id",
            "is_active",
            "is_author",
            "hour",
            "language",
            "user",
            "classes",
            "quarter",
            "science",
            "class_group",
            "science_types",
            "is_topic",
            "created_at",
        ]

    def get_is_author(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return obj.user == request.user
        return False

    def get_user(self, obj):
        from core.http.serializers import UserSerializer

        return UserSerializer(obj.user).data

    def get_is_topic(self, obj):
        return Topic.objects.filter(plan_id=obj.id).exists()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get("request")

        if request and request.user.is_authenticated:
            data["is_author"] = instance.user == request.user

        return data
