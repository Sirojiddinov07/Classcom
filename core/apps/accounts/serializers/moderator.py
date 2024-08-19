from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.utils.translation import gettext as _
from rest_framework import serializers, exceptions

from core.apps.classcom.choices import Degree
from core.apps.classcom.models import Moderator
from core.apps.classcom.models import ScienceTypes
from core.http import models
from core.services import UserService


class ModeratorSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(max_length=255)
    science_types = serializers.ListField(
        child=serializers.PrimaryKeyRelatedField(
            queryset=ScienceTypes.objects.all()
        )
    )
    degree = serializers.ChoiceField(choices=Degree.choices)
    docs = serializers.FileField()

    def validate_phone(self, value):
        user = models.User.objects.filter(
            phone=value, validated_at__isnull=False
        )
        if user.exists():
            raise exceptions.ValidationError(
                _("Phone number already registered."), code="unique"
            )
        return value

    def create(self, data):
        try:
            docs = self.context.get("request").FILES["docs"]
            file = default_storage.save(docs.name, ContentFile(docs.read()))
            user = UserService().create_user(
                phone=data.get("phone"),
                password=data.get("password"),
                last_name=data.get("last_name"),
                first_name=data.get("first_name"),
                district_id=data.get("district").id,
                region_id=data.get("region").id,
                institution=data.get("institution"),
                institution_number=data.get("institution_number"),
                science_id=data.get("science").id,
                school_type_id=data.get("school_type").id,
                role="user",
            )
            return Moderator.objects.update_or_create(
                user=user,
                defaults={"degree": data.get("degree"), "docs": file},
            )
        except Exception as e:
            raise exceptions.ValidationError({"detail": e})

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
            "science",
            "science_types",
            "degree",
            "docs",
        ]
        extra_kwargs = {
            "first_name": {"required": True},
            "role": {"read_only": True},
            "password": {"write_only": True},
            "degree": {"required": False},
            "science": {"required": True},
            "last_name": {"required": True},
            "district": {"required": True},
            "region": {"required": True},
            "institution_number": {"required": True},
        }
