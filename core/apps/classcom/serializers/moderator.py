from rest_framework import serializers
from core.apps.classcom import models
from django.utils.translation import gettext as _
from core.http import choices
from core.apps.classcom.serializers import RegionSerializer,DistrictSerializer


class UserModeratorSerializer(serializers.ModelSerializer):
    _region = RegionSerializer(read_only=True,source="region")
    _district = DistrictSerializer(read_only=True,source="district")

    class Meta:
        model = models.User
        fields = [
            "first_name", "last_name",
              "phone", "password",
                "_region", "_district",
                "region","district",
                  "institution","institution_number"
                  ]

    def validate_phone(self, value):
        user = models.User.objects.filter(phone=value, validated_at__isnull=False)
        if user.exists():
            raise serializers.ValidationError(_("Phone number already registered."), code='unique')
        return value

    def create(self, validated_data):
        region_data = validated_data.pop('region')
        district_data = validated_data.pop('district')

        region, _ = choices.Region.objects.get_or_create(**region_data)
        district_data.pop('region', None)  # Ensure 'region' is not in district_data
        district, _ = choices.District.objects.get_or_create(region=region, **district_data)

        user = models.User.objects.create(region=region, district=district, **validated_data)
        return user


class ModeratorCreateSerializer(serializers.ModelSerializer):
    user = UserModeratorSerializer()

    class Meta:
        model = models.Moderator
        fields = ["user", "science", "classes", "degree", "docs"]

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user_serializer = UserModeratorSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()
        moderator = models.Moderator.objects.create(user=user, **validated_data)
        return moderator
