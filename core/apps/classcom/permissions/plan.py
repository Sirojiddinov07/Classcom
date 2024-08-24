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
        try:
            moderator = Moderator.objects.get(user=user)
            if not moderator.plan_creatable:
                raise ValidationError("User is not allowed to create a plan.")
        except Moderator.DoesNotExist:
            raise ValidationError("User is not a Moderator.")
        return user.role in self.roles
