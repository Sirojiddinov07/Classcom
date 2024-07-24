from rest_framework import serializers

from core.apps.classcom import models, services
from core.http.models import User

from ..serializers.classes import ClassMiniSerializer
from ..serializers.media import MediaSerializer
from ..serializers.quarter import QuarterMiniSerializer
from ..serializers.science import ScienceMiniSerializer
from ..serializers.topic import TopicMiniSerializer


class PlanScienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Science
        fields = ("id", "name")


class PlanQuarterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Quarter
        fields = ("id", "choices", "start_date", "end_date")


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ResourceType
        fields = ("id", "name")


class PlanClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Classes
        fields = ("id", "name")


class PlanTopicSerializer(serializers.ModelSerializer):
    quarter = PlanQuarterSerializer()
    science = PlanScienceSerializer()

    class Meta:
        model = models.Topic
        fields = ("id", "name", "quarter", "science")


###############################################################################
# Plan Detail Serializer
###############################################################################
class UserMiniSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["first_name", "last_name"]


class PlanDetailSerializer(serializers.ModelSerializer):
    type = TypeSerializer()
    classes = PlanClassSerializer()
    topic = PlanTopicSerializer()
    quarter = PlanQuarterSerializer()
    science = PlanScienceSerializer()
    plan_resource = MediaSerializer(many=True, read_only=True)
    is_author = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    user = UserMiniSerializer()

    class Meta:
        model = models.Plan
        fields = (
            "id",
            "name",
            "description",
            "banner",
            "classes",
            "topic",
            "type",
            "quarter",
            "science",
            "plan_resource",
            "status",
            "user",
            "is_author",
            "created_at",
        )

    def get_status(self, obj):
        return "active"

    def get_is_author(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return obj.user == request.user
        return False

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            data["is_author"] = instance.user == request.user
        return data


class PlanSerializer(serializers.ModelSerializer):
    type = TypeSerializer()
    classes = PlanClassSerializer()
    topic = PlanTopicSerializer()
    quarter = PlanQuarterSerializer()
    science = PlanScienceSerializer()
    plan_resource = MediaSerializer(many=True, read_only=True)
    is_author = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    user = UserMiniSerializer()

    class Meta:
        model = models.Plan
        fields = (
            "id",
            "name",
            "description",
            "banner",
            "classes",
            "topic",
            "type",
            "quarter",
            "science",
            "hour",
            "plan_resource",
            "status",
            "user",
            "is_author",
            "created_at",
        )

    def get_status(self, obj):
        return "active"

    def get_is_author(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return obj.user == request.user
        return False

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            data["is_author"] = instance.user == request.user
        return data


###########################################################
# Plan Create Serializer
###########################################################
class PlanCreateSerializer(serializers.ModelSerializer):
    _topic = TopicMiniSerializer(read_only=True, source="topic")
    _class = ClassMiniSerializer(read_only=True, source="classes")
    _quarter = QuarterMiniSerializer(read_only=True, source="quarter")
    _science = ScienceMiniSerializer(read_only=True, source="science")

    class Meta:
        model = models.Plan
        fields = (
            "id",
            "name",
            "description",
            "banner",
            "type",
            "topic",
            "classes",
            "quarter",
            "science",
            "hour",
            "_topic",
            "_class",
            "_quarter",
            "_science",
        )
        extra_kwargs = {"classes": {"write_only": True}}

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return services.BaseService().serializer_name_replace(
            data,
            [
                "_topic",
                "_class",
                "_quarter",
                "_science",
            ],
        )

    def create(self, validated_data):
        validated_data.pop("user", None)

        resource = models.Plan.objects.create(
            user=self.context["request"].user, **validated_data
        )
        return resource


class PlanSetMediaSerializer(serializers.Serializer):
    _media = MediaSerializer(many=True, read_only=True, source="plan_resource")
    media = serializers.ListField(
        child=serializers.FileField(), write_only=True
    )
    names = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
    )
    descriptions = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
    )
