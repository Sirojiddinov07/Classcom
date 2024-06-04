from rest_framework import serializers
from core.apps.classcom import models
from django.utils.translation import gettext as _
from core.http import models as http_models
from core.apps.classcom.serializers import RegionSerializer, DistrictSerializer
from rest_framework.exceptions import APIException


class UserModeratorSerializer(serializers.ModelSerializer):
    _region = RegionSerializer(read_only=True, source="region")
    _district = DistrictSerializer(read_only=True, source="district")

    class Meta:
        model = models.User
        fields = [
            "first_name",
            "last_name",
            "phone",
            "password",
            "_region",
            "_district",
            "region",
            "district",
            "institution",
            "institution_number",
        ]
        extra_kwargs = {
            "region": {
                "write_only": True,
            },
            "district": {
                "write_only": True,
            },
        }

    def validate_phone(self, value):
        user = models.User.objects.filter(
            phone=value, validated_at__isnull=False
        )
        if user.exists():
            raise serializers.ValidationError(
                _("Phone number already registered."), code="unique"
            )
        return value


class ModeratorCreateSerializer(serializers.ModelSerializer):
    user = UserModeratorSerializer()

    class Meta:
        model = models.Moderator
        fields = ["user", "science", "classes", "degree", "docs"]

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user_data["region"] = user_data["region"].id
        user_data["district"] = user_data["district"].id
        user_serializer = UserModeratorSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()
        moderator = models.Moderator.objects.create(
            user=user, **validated_data
        )
        return moderator
