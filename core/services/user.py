import typing
from datetime import datetime

from django.contrib.auth import hashers
from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt import tokens
from core.apps.classcom.choices import Role

from core import exceptions
from core.http import models
from core.services import base_service, sms
from core.utils import exception
from core.http.models import ScienceGroups


class UserService(base_service.BaseService, sms.SmsService):
    def get_token(self, user):
        refresh = tokens.RefreshToken.for_user(user)

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

    def create_user(self, phone, first_name, last_name, password, region_id, district_id, institution,
                    institution_number, science_group_id=None, science_id=None, role=Role.USER):
        region = get_object_or_404(models.Region, id=region_id)
        district = get_object_or_404(models.District, id=district_id)

        science_group = None if science_group_id is None else get_object_or_404(ScienceGroups, id=science_group_id)
        science = None if science_id is None else get_object_or_404(models.Science, id=science_id)

        user, _ = models.User.objects.update_or_create(
            phone=phone,
            defaults={
                "phone": phone,
                "first_name": first_name,
                "last_name": last_name,
                "password": hashers.make_password(password),
                "role": role,
                "region": region,
                "district": district,
                "institution": institution,
                "institution_number": institution_number,
                "science_group": science_group,
                "science": science,
            },
        )
        return user

    def send_confirmation(self, phone) -> bool:
        try:
            self.send_confirm(phone)
            return True
        except exceptions.SmsException as e:
            exception.ResponseException(
                e, data={"expired": e.kwargs.get("expired")}
            )  # noqa
        except Exception as e:
            exception.ResponseException(e)

    def validate_user(self, user: typing.Union[models.User]) -> dict:
        """
        Create user if user not found
        """
        user.validated_at = datetime.now()
        user.save()
        token = self.get_token(user)
        return token

    def is_validated(self, user: typing.Union[models.User]) -> bool:
        """
        User is validated check
        """
        if user.validated_at is not None:
            return True
        return False

    def change_password(self, phone, password):
        """
        Change password
        """
        user = models.User.objects.filter(phone=phone).first()
        user.set_password(password)
        user.save()
