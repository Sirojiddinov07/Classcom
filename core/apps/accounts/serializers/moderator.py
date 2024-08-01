from rest_framework import serializers
from core.apps.classcom.models import Science, Classes, Moderator
from core.apps.classcom.choices import Degree
from core.http.serializers import RegisterSerializer
from core.services import UserService
from django.utils.translation import gettext as _


class ModeratorSerializer(serializers.Serializer):
    user = RegisterSerializer()
    science = serializers.PrimaryKeyRelatedField(queryset=Science.objects.all())
    classes = serializers.PrimaryKeyRelatedField(queryset=Classes.objects.all())
    degree = serializers.ChoiceField(choices=Degree.choices)

    def validate_user(self, value):
        phone = value.get("phone")
        if Moderator.objects.filter(user__phone=phone, user__validated_at__isnull=False):
            raise serializers.ValidationError(_("Moderator Already This user"))
        return value

    def create(self, validated_data):
        user = validated_data.pop("user")
        user = UserService().create_user(
            phone=user.get("phone"),
            password=user.get("password"),
            last_name=user.get("last_name"),
            first_name=user.get("first_name"),
            district_id=user.get("district").id,
            region_id=user.get("region").id,
            institution=user.get("institution"),
            institution_number=user.get("institution_number"),
        )
        return Moderator.objects.update_or_create(
            user=user,
            defaults={
                "science": validated_data.get("science"),
                "classes": validated_data.get("classes"),
                "degree": validated_data.get("degree")
            }
        )
