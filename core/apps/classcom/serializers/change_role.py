from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from core.apps.classcom.models import (
    TempModerator,
    choices,
)
from core.http.models import User


class ChangeRoleSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()

    class Meta:
        model = TempModerator
        fields = [
            "user_id",
            "balance",
            "degree",
            "docs",
            "is_contracted",
        ]

    def validate_user_id(self, value):
        request = self.context.get("request")
        if not request or not request.user:
            raise serializers.ValidationError(
                {
                    "detail": _("Foydalanuvchi soʻrovi mavjud emas"),
                    "code": "no_request_user",
                }
            )

        try:
            user = User.objects.get(id=value)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                {
                    "detail": _("Foydalanuvchi topilmadi"),
                    "code": "user_not_found",
                }
            )

        if user.role == choices.Role.MODERATOR:
            raise serializers.ValidationError(
                {
                    "detail": _("Foydaluvchi allaqachon moderator"),
                    "code": "already_moderator",
                }
            )

        # Ensure only the requesting user can change their role
        if user != request.user:
            raise serializers.ValidationError(
                {
                    "detail": _(
                        "Siz faqat o'zingizning ro'lingizni o'zgartirishingiz mumkin"
                    ),
                    "code": "permission_denied",
                }
            )

        return value

    def create(self, validated_data):
        user_id = validated_data.pop("user_id")
        user = User.objects.get(id=user_id)
        moderator = TempModerator.objects.create(user=user, **validated_data)
        return moderator
