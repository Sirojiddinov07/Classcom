from rest_framework import serializers

from core.apps.classcom.models.electron_resource import (
    ElectronResource,
    ElectronResourceCategory,
    ElectronResourceSubCategory,
)


class ElectronResourceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ElectronResourceCategory
        fields = "__all__"


class ElectronResourceSubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ElectronResourceSubCategory
        fields = "__all__"


class ElectronResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElectronResource
        fields = "__all__"
