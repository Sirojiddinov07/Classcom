from rest_framework import serializers

from core.apps.classcom import models
from core.apps.classcom.serializers import media


class PlanScienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Science
        fields = ('id', 'name')


class PlanQuarterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Quarter
        fields = ('id', 'name')


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ResourceType
        fields = ('id', 'name')


class PlanClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Classes
        fields = ('id', 'name')


class PlanTopicSerializer(serializers.ModelSerializer):
    quarter = PlanQuarterSerializer()
    science = PlanScienceSerializer()

    class Meta:
        model = models.Topic
        fields = ('id', 'name', 'quarter', 'science')


##############################################################################################################
# Plan Detail Serializer
##############################################################################################################
class PlanDetailSerializer(serializers.ModelSerializer):
    type = TypeSerializer()
    classes = PlanClassSerializer()
    topic = PlanTopicSerializer()
    quarter = PlanQuarterSerializer()
    science = PlanScienceSerializer()
    media = media.MediaSerializer(many=True, read_only=True)

    class Meta:
        model = models.Plan
        fields = (
            "id", "name", "description", "banner",
            "classes", "topic", "media", "type", "quarter", "science"
        )


##############################################################################################################
# Plan Create Serializer
##############################################################################################################
class PlanCreateSerializer(serializers.ModelSerializer):
    plan_resource = media.MediaSerializer(many=True)

    class Meta:
        model = models.Plan
        fields = (
            'name', 'description', 'banner', 'type', 'topic', 'classes', 'quarter', 'science', 'hour', 'plan_resource')

    def create(self, validated_data):
        media_data = validated_data.pop('media')
        validated_data.pop('user', None)
        resource = models.Plan.objects.create(user=self.context['request'].user, **validated_data)
        for media_item in media_data:
            models.Media.objects.create(resource=resource, **media_item)
        return resource

# class PlanSerializer(serializers.ModelSerializer):
#     type_id = serializers.SerializerMethodField()
#     type_name = serializers.SerializerMethodField()
#     class_id = serializers.SerializerMethodField()
#     class_name = serializers.SerializerMethodField()
#     topic_id = serializers.SerializerMethodField()
#     topic_name = serializers.SerializerMethodField()
#     quarter_id = serializers.SerializerMethodField()
#     quarter_name = serializers.SerializerMethodField()
#     science_id = serializers.SerializerMethodField()
#     science_name = serializers.SerializerMethodField()
#     media = media.MediaSerializer(many=True, read_only=True)
#
#     class Meta:
#         model = models.Resource
#         fields = (
#             "id", "name", "description", "banner",
#             "class_id", "class_name",
#             "topic_id", "topic_name",
#             "quarter_id", "quarter_name",
#             "science_id", "science_name",
#             "media", "type_id", "type_name"
#         )
#
#     def get_type_id(self, obj):
#         return obj.type.id
#
#     def get_type_name(self, obj):
#         return obj.type.name
#
#     def get_class_id(self, obj):
#         return obj.classes.id
#
#     def get_class_name(self, obj):
#         return obj.classes.name
#
#     def get_topic_id(self, obj):
#         return obj.topic.id
#
#     def get_topic_name(self, obj):
#         return obj.topic.name
#
#     def get_quarter_id(self, obj):
#         return obj.topic.quarter.id
#
#     def get_quarter_name(self, obj):
#         return obj.topic.quarter.name
#
#     def get_science_id(self, obj):
#         return obj.topic.science.id
#
#     def get_science_name(self, obj):
#         return obj.topic.science.name
