from rest_framework import serializers
from ..models import ResourceType, Classes
from ..choices import Types, Departments, Schools, Docs


class ResourceTypeSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()
    label = serializers.SerializerMethodField()

    def get_label(self, obj):
        return obj.get_type_display()

    def get_items(self, obj):
        response = []
        match obj.type:
            case Types.BYCLASS | Types.BYCLASSANDUNIT:
                response = Classes.objects.all().values_list("id", "name")
            case Types.BYDEPARTMENT:
                response = [{"id": i.name, "name": str(i.label)} for i in Departments]
            case Types.BYSCHOOL:
                response = [{"id": i.name, "name": str(i.label)} for i in Schools]
            case Types.BYDOCS:
                response = [{"id": i.name, "name": str(i.label)} for i in Docs]
        return response

    class Meta:
        model = ResourceType
        fields = (
            "id",
            "name",
            "type",
            "label",
            "items",
        )


class ResourceTypeMiniSerializer(serializers.ModelSerializer):
    label = serializers.SerializerMethodField()

    def get_label(self, obj):
        return obj.get_type_display()

    class Meta:
        model = ResourceType
        fields = (
            "id",
            "name",
            "label",
        )
