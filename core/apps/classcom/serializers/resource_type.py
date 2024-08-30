from rest_framework import serializers

from ..choices import Types, Departments, Schools, Docs
from ..models import ResourceType, Classes, Science


class ResourceTypeSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()
    label = serializers.SerializerMethodField()

    def get_label(self, obj):
        return obj.get_type_display()

    def get_items(self, obj):
        response = []
        match obj.type:
            case Types.BYCLASS | Types.BYCLASSANDUNIT:
                response = Classes.objects.all().values("id", "name")
            case Types.BYDEPARTMENT:
                response = [
                    {"id": i.name, "name": str(i.label)} for i in Departments
                ]
            case Types.BYSCHOOL:
                response = [
                    {"id": i.name, "name": str(i.label)} for i in Schools
                ]
            case Types.BYDOCS:
                response = [{"id": i.name, "name": str(i.label)} for i in Docs]
            case Types.BYSCIENCE:
                response = Science.objects.all().values("id", "name")
        return response

    class Meta:
        model = ResourceType
        fields = ("id", "name", "type", "label", "items", "is_active")


class ResourceTypeMiniSerializer(serializers.ModelSerializer):
    label = serializers.SerializerMethodField()

    def get_label(self, obj):
        return obj.get_type_display()

    class Meta:
        model = ResourceType
        fields = ("id", "name", "label", "is_active")
