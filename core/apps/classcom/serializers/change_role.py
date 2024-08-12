from rest_framework import serializers
from core.apps.classcom.models import (
    TempModerator,
    choices,
    Science,
    ScienceTypes,
)
from core.http.models import User


class ChangeRoleSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()
    science_id = serializers.PrimaryKeyRelatedField(
        queryset=Science.objects.all(), source="science", allow_null=True
    )
    science_type_id = serializers.PrimaryKeyRelatedField(
        queryset=ScienceTypes.objects.all(),
        source="science_type",
        allow_null=True,
    )

    class Meta:
        model = TempModerator
        fields = [
            "user_id",
            "balance",
            "degree",
            "docs",
            "is_contracted",
            "science_id",
            "science_type_id",
        ]

    def validate_user_id(self, value):
        request = self.context.get("request")
        if not request or not request.user:
            raise serializers.ValidationError(
                {
                    "detail": "Request user is not available",
                    "code": "no_request_user",
                }
            )

        try:
            user = User.objects.get(id=value)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                {"detail": "User not found", "code": "user_not_found"}
            )

        if user.role == choices.Role.MODERATOR:
            raise serializers.ValidationError(
                {
                    "detail": "User is already a moderator",
                    "code": "already_moderator",
                }
            )

        # Ensure only the requesting user can change their role
        if user != request.user:
            raise serializers.ValidationError(
                {
                    "detail": "You do not have permission to change this user's role",
                    "code": "permission_denied",
                }
            )

        return value

    def create(self, validated_data):
        user_id = validated_data.pop("user_id")
        user = User.objects.get(id=user_id)
        moderator = TempModerator.objects.create(user=user, **validated_data)
        return moderator
