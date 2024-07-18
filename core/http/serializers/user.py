from django.conf import settings
from rest_framework import serializers

from core.http import models


class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(max_length=None, use_url=True)
    permissions = serializers.SerializerMethodField()

    class Meta:
        fields = [
            "avatar",
            "first_name",
            "last_name",
            "phone",
            "role",
            "region",
            "district",
            "science_group",
            "permissions"
        ]
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

    def get_permissions(self, obj):
        request = self.context.get('request', None)
        user = self.context.get("user", None)
        if request is None and user is None:
            return []

        if request:
            user = request.user

        groups = user.groups.all()
        permissions = []
        for group in groups:
            for permission in group.permissions.all():
                permissions.append(permission.name)
        for permission in user.get_user_permissions():
            permissions.append(permission)
        return permissions

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
