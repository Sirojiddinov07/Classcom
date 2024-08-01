from rest_framework import serializers
from core.apps.classcom.models import TempModerator, choices
from core.http.models import User


class ChangeRoleSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()

    class Meta:
        model = TempModerator
        fields = ["user_id", "balance", "degree", "docs", "is_contracted"]

    def validate_user_id(self, value):
        try:
            user = User.objects.get(id=value)
        except User.DoesNotExist:
            raise serializers.ValidationError({"detail": "User not found", "code": "user_not_found"})
        if user.role == choices.Role.MODERATOR:
            raise serializers.ValidationError({"detail": "User is already a moderator", "code": "already_moderator"})
        return value

    def create(self, validated_data):
        user_id = validated_data.pop('user_id')
        user = User.objects.get(id=user_id)
        moderator = TempModerator.objects.create(user=user, **validated_data)
        return moderator
