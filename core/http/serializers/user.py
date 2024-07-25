from django.conf import settings
from rest_framework import serializers
from core.utils import Role


from core.apps.classcom.choices import Role
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
            "science",
            "classes",
            "permissions",
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
        request = self.context.get("request", None)
        user = self.context.get("user", None)
        if request is None and user is None:
            return []

        if request:
            user = request.user

        return Role(user).get_permissions()

    def update(self, instance, validated_data):
        print(validated_data)  # Debug line
        instance.avatar = validated_data.get("avatar", instance.avatar)
        instance.first_name = validated_data.get(
            "first_name", instance.first_name
        )
        instance.last_name = validated_data.get(
            "last_name", instance.last_name
        )
        instance.region = validated_data.get("region", instance.region)
        instance.district = validated_data.get("district", instance.district)
        instance.science_group = validated_data.get(
            "science_group", instance.science_group
        )
        instance.science = validated_data.get("science", instance.science)
        instance.classes = validated_data.get("classes", instance.classes)
        instance.save()
        return instance


class UserRoleChangeSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=Role)

    class Meta:
        model = models.User
        fields = ["role"]
