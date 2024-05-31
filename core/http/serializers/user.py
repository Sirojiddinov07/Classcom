from django.conf import settings

from rest_framework import serializers

from core.http import models


class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField('get_avatar')
    class Meta:
        fields = ["avatar","first_name", "last_name", "phone", 'role']
        model = models.User
            
    def get_avatar(self, obj):
        if obj.avatar:
            avatar_url = obj.avatar.url.replace(settings.MEDIA_URL, '')
            media_url = settings.MEDIA_URL if settings.MEDIA_URL.endswith("/") else settings.MEDIA_URL + "/"
            return media_url + avatar_url
        return None
    
    def update(self, instance, validated_data):
        instance.avatar = validated_data.get(
            'avatar', instance.avatar
        )
        instance.first_name = validated_data.get(
            "first_name", instance.first_name
        )
        instance.last_name = validated_data.get(
            "last_name", instance.last_name
        )
        instance.phone = validated_data.get("phone", instance.phone)
        instance.save()
        return instance
