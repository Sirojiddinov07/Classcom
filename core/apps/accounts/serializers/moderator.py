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
    docs = serializers.ListField(
        child=serializers.FileField(), write_only=True
    )
    role = serializers.CharField(read_only=True, default="moderator")

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
            docs_files = self.context.get("request").FILES.getlist("docs")
            saved_files = []
            for doc in docs_files:
                file = default_storage.save(doc.name, ContentFile(doc.read()))
                saved_files.append(file)
            user = UserService().create_user(
                phone=data.get("phone"),
                first_name=data.get("first_name"),
                last_name=data.get("last_name"),
                password=data.get("password"),
                region_id=data.get("region").id,
                district_id=data.get("district").id,
                institution=data.get("institution"),
                institution_number=data.get("institution_number"),
                science_group_id=data.get("science_group"),
                science_id=data.get("science").id,
                role=data.get("role"),
                school_type_id=data.get("school_type").id,
                class_group_id=data.get("class_group").id,
            )
            moderator, created = Moderator.objects.update_or_create(
                user=user, defaults={"degree": data.get("degree")}
            )
            moderator.docs.set(saved_files)
            return moderator
        except Exception as e:
            raise exceptions.ValidationError({"detail": str(e)})

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
            "school_type",
            "class_group",
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
            "class_group": {"required": True},
            "institution_number": {"required": True},
        }
