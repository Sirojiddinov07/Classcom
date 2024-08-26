from django.utils.translation import gettext_lazy as _
from rest_framework import permissions
from rest_framework.exceptions import ValidationError

from core.apps.classcom.models import Moderator


class PlanPermission(permissions.BasePermission):
    message = _("Sizda bu amalni bajarish uchun ruxsat yo‘q.")

    def __init__(self, roles: list) -> None:
        super().__init__()
        self.roles = roles

    def __call__(self, *args, **kwargs):
        return self

    def has_permission(self, request, view):
        user = request.user
        languages = request.data.get("language")
        science = request.data.get("science")
        science_type = request.data.get("science_types")
        classes = request.data.get("classes")
        class_groups = request.data.get("class_group")
        quarters = request.data.get("quarter")

        try:
            moderator = Moderator.objects.get(user=user)
            if (
                not moderator.plan_creatable
                and moderator.languages.filter(id=languages).exists()
                and moderator.science.filter(id=science).exists()
                and moderator.science_type.filter(id=science_type).exists()
                and moderator.classes.filter(id=classes).exists()
                and moderator.class_groups.filter(id=class_groups).exists()
                and moderator.quarters.filter(id=quarters).exists()
            ):
                raise ValidationError("User is not allowed to create a plan.")
        except Moderator.DoesNotExist:
            raise ValidationError("User is not a Moderator.")

        return user.role in self.roles
