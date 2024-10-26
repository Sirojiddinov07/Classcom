import logging

from django.utils.translation import gettext as _
from rest_framework import serializers, exceptions
from rest_framework import status
from rest_framework.response import Response

from core.apps.classcom.choices import Degree
from core.apps.classcom.models import Moderator, Document
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
    # role = serializers.CharField(read_only=True, default="moderator")

    def validate_phone(self, value):
        user = models.User.objects.filter(phone=value)
        if user.exists():
            raise exceptions.ValidationError(
                _("Phone number already registered."), code="unique"
            )
        return value

    def create(self, data):
        try:
            request = self.context.get("request")
            docs_data = []

            for key in request.data:
                if key.startswith("description[") and key.endswith("]"):
                    index = key[len("description[") : -1]  # noqa: E203
                    file_key = f"docs[{index}]"
                    doc_desc = request.data.get(key)
                    doc_file = request.FILES.get(file_key)

                    if not doc_file:
                        return Response(
                            {
                                "error": f"File is required for document item {index}"
                            },
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                    if not doc_desc:
                        doc_desc = doc_file.name
                    docs_data.append(
                        {"docs": doc_file, "description": doc_desc}
                    )

            user = UserService().create_user(
                phone=data.get("phone"),
                first_name=data.get("first_name"),
                last_name=data.get("last_name"),
                father_name=data.get("father_name"),
                password=data.get("password"),
                region_id=data.get("region").id,
                district_id=data.get("district").id,
                institution=data.get("institution"),
                institution_number=data.get("institution_number"),
                science_group_id=data.get("science_group"),
                science_id=data.get("science").id,
                # role=data.get("role"),
                school_type_id=data.get("school_type"),
                class_group_id=data.get("class_group").id,
            )

            moderator, created = Moderator.objects.update_or_create(
                user=user, defaults={"degree": data.get("degree")}
            )

            for doc_data in docs_data:
                document = Document.objects.create(
                    file=doc_data["docs"], description=doc_data["description"]
                )
                moderator.docs.add(document)

            return moderator
        except Exception as e:
            logging.error(f"Error in create method: {str(e)}")
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
        }
