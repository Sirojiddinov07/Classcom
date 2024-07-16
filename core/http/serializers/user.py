from django.conf import settings
from rest_framework import serializers

from core.apps.classcom.choices import Role
from core.http import models


class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(max_length=None, use_url=True)

    class Meta:
        fields = ["avatar", "first_name", "last_name", "phone", "role", "region", "district", "science_group"]
        extra_kwargs = {
            "role": {"read_only": True},
        }
        model = models.User

    def get_avatar(self, obj):
        if obj.avatar:
            avatar_url = obj.avatar.url.replace(settings.MEDIA_URL, "")
            media_url = (
                settings.MEDIA_URL
                if settings.MEDIA_URL.endswith("/")
                else settings.MEDIA_URL + "/"
            )
            return media_url + avatar_url
        return None

    def update(self, instance, validated_data):
        print(validated_data)  # Debug line
        instance.avatar = validated_data.get("avatar", instance.avatar)
        instance.first_name = validated_data.get(
            "first_name", instance.first_name
        )
        instance.last_name = validated_data.get(
            "last_name", instance.last_name
        )
        instance.save()
        return instance


class UserRoleChangeSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=Role)

    class Meta:
        model = models.User
        fields = ["role"]
