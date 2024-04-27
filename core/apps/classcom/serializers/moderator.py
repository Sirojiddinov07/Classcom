from rest_framework import serializers
from core.apps.classcom import models
from django.utils.translation import gettext as _
from core.http import choices


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = choices.Region
        fields = ["region"]


class DistrictSerializer(serializers.ModelSerializer):
    region = RegionSerializer()

    class Meta:
        model = choices.District
        fields = ["district", "region"]


class UserSerializer(serializers.ModelSerializer):
    region = RegionSerializer()
    district = DistrictSerializer()

    class Meta:
        model = models.User
        fields = ["first_name", "last_name", "phone", "password", "region", "district", "institution",
                  "institution_number"]

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
    user = UserSerializer()

    class Meta:
        model = models.Moderator
        fields = ["user", "science", "classes", "degree", "docs"]

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()
        moderator = models.Moderator.objects.create(user=user, **validated_data)
        return moderator
