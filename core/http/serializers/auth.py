from django.utils.translation import gettext as _
from rest_framework import exceptions, serializers

from core.apps.classcom.choices import Degree
from core.apps.classcom.models import ScienceTypes
from core.http import models


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)


class RegisterSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(max_length=255)
    science_types = serializers.ListField(
        child=serializers.PrimaryKeyRelatedField(
            queryset=ScienceTypes.objects.all()
        )
    )
    degree = serializers.ChoiceField(choices=Degree.choices, required=False)
    role = serializers.CharField(read_only=True, default="user")

    def validate_phone(self, value):
        user = models.User.objects.filter(
            phone=value, validated_at__isnull=False
        )
        if user.exists():
            raise exceptions.ValidationError(
                _("Phone number already registered."), code="unique"
            )
        return value

    class Meta:
        model = models.User
        fields = [
            "first_name",
            "last_name",
            "phone",
            "password",
            "role",
            "region",
            "district",
            "institution",
            "institution_number",
            "science_group",
            "science",
            "science_types",
            "degree",
            "school_type",
        ]
        extra_kwargs = {
            "first_name": {"required": True},
            "role": {"read_only": True},
            "password": {"write_only": True},
            "degree": {"required": False},
            "science": {"required": True},
            "last_name": {"required": True},
        }


class ConfirmSerializer(serializers.Serializer):
    code = serializers.IntegerField(min_value=1000, max_value=9999)
    phone = serializers.CharField(max_length=255)


class ResetPasswordSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=255)

    def validate_phone(self, value):
        user = models.User.objects.filter(phone=value)
        if user.exists():
            return value

        raise serializers.ValidationError(_("Foydalanuvchi topilmadi"))


class ResetConfirmationSerializer(serializers.Serializer):
    code = serializers.IntegerField(min_value=1000, max_value=9999)
    phone = serializers.CharField(max_length=255)

    def validate_phone(self, value):
        user = models.User.objects.filter(phone=value)
        if user.exists():
            return value
        raise serializers.ValidationError(_("User does not exist"))


class ResendSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=255)
