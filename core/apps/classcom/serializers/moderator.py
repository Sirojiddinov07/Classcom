from django.utils.translation import gettext as _
from rest_framework import serializers

from core.apps.classcom import models
from core.http.models import District, Region
from core.services import UserService

from ..serializers.district import DistrictSerializer
from ..serializers.region import RegionSerializer


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
        if models.User.objects.filter(
            phone=value, validated_at__isnull=False
        ).exists():
            raise serializers.ValidationError(
                _("Phone number already registered."), code="unique"
            )
        return value

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = models.User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


class ModeratorCreateSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    phone = serializers.CharField(source="user.phone", required=True)
    password = serializers.CharField(
        source="user.password", write_only=True, required=True
    )
    region = serializers.PrimaryKeyRelatedField(
        queryset=Region.objects.all(), source="user.region"
    )
    district = serializers.PrimaryKeyRelatedField(
        queryset=District.objects.all(), source="user.district"
    )
    institution = serializers.CharField(source="user.institution")
    institution_number = serializers.CharField(
        source="user.institution_number"
    )

    class Meta:
        model = models.Moderator
        fields = [
            "first_name",
            "last_name",
            "phone",
            "password",
            "region",
            "district",
            "institution",
            "institution_number",
            "science",
            "classes",
            "degree",
            "docs",
        ]

    def create(self, validated_data):
        user_data = validated_data.pop("user")

        region = user_data.pop("region")
        district = user_data.pop("district")

        user_data["region"] = region.id
        user_data["district"] = district.id

        user_serializer = UserModeratorSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()

        sms_service = UserService()
        sms_service.send_confirmation(user.phone)

        moderator = models.Moderator.objects.create(
            user=user, **validated_data
        )
        return moderator
