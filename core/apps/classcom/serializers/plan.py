from rest_framework import serializers

from core.apps.classcom.models import Plan
from core.apps.classcom.serializers.classes import ClassesSerializer
from core.apps.classcom.serializers.quarter import QuarterMiniSerializer
from core.apps.classcom.serializers.science import ScienceSerializer
from core.apps.classcom.serializers.science import ScienceTypesSerializer
from core.apps.classcom.serializers.topic import TopicDetailSerializer
from core.apps.classcom.serializers.type import TypeSerializer
from core.http.serializers import UserSerializer, ClassGroupSerializer


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = [
            "id",
            "language",
            "type",
            "classes",
            "quarter",
            "science",
            "class_group",
            "science_types",
        ]

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["user"] = user

        plan = Plan.objects.create(**validated_data)
        return plan


class PlanDetailSerializer(serializers.ModelSerializer):
    type = TypeSerializer()
    classes = ClassesSerializer()
    user = UserSerializer()
    quarter = QuarterMiniSerializer()
    science = ScienceSerializer()
    class_group = ClassGroupSerializer()
    science_types = ScienceTypesSerializer()
    is_author = serializers.SerializerMethodField()
    topic = TopicDetailSerializer(many=True)

    class Meta:
        model = Plan
        fields = [
            "id",
            "is_active",
            "is_author",
            "hour",
            "language",
            "type",
            "user",
            "classes",
            "quarter",
            "science",
            "class_group",
            "science_types",
            "topic",
            "created_at",
        ]
        extra_kwargs = {"topic": {"required": False}}

    def get_is_author(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return obj.user == request.user
        return False

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get("request")

        if request.user.is_authenticated:
            data["is_author"] = instance.user == request.user

        return data
