from django.utils.translation import gettext as _
from rest_framework import serializers

from core.apps.classcom.models import Moderator
from core.http.models import District, Region, User
from core.services import UserService
from ..serializers.district import DistrictSerializer
from ..serializers.region import RegionSerializer


class UserModeratorSerializer(serializers.ModelSerializer):
    _region = RegionSerializer(read_only=True, source="region")
    _district = DistrictSerializer(read_only=True, source="district")

    # Delayed import inside the class
    def __init__(self, *args, **kwargs):
        from core.apps.classcom.serializers import (
            RegionSerializer,
            DistrictSerializer,
        )

        self.RegionSerializer = RegionSerializer
        self.DistrictSerializer = DistrictSerializer
        super().__init__(*args, **kwargs)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret["_region"] = self.RegionSerializer(
            instance.region, read_only=True
        ).data
        ret["_district"] = self.DistrictSerializer(
            instance.district, read_only=True
        ).data
        return ret

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "father_name",
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
        if User.objects.filter(
            phone=value, validated_at__isnull=False
        ).exists():
            raise serializers.ValidationError(
                _("Telfon raqam allaqachon ro'yxatdan o'tgan."), code="unique"
            )
        return value

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


class ModeratorCreateSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    father_name = serializers.CharField(
        source="user.father_name", required=False
    )
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
    institution_number = serializers.CharField(
        source="user.institution_number"
    )
    institution = serializers.CharField(source="user.institution")

    class Meta:
        model = Moderator
        fields = [
            "first_name",
            "last_name",
            "father_name",
            "phone",
            "password",
            "region",
            "district",
            "institution",
            "institution_number",
            "science",
            "science_type",
            "degree",
            "docs",
            "is_contracted",
        ]

    def create(self, validated_data):
        language = self.context.get("request").headers.get(
            "Accept-Language", "uz"
        )
        user_data = validated_data.pop("user")
        region = user_data.pop("region")
        district = user_data.pop("district")

        user_data["region"] = region.id
        user_data["district"] = district.id

        user_serializer = UserModeratorSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()

        sms_service = UserService()
        sms_service.send_confirmation(user.phone, language)

        moderator = Moderator.objects.create(user=user, **validated_data)
        return moderator
