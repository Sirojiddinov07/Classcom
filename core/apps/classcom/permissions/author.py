from django.utils.translation import gettext_lazy as _
from rest_framework import permissions


class IsAuthor(permissions.BasePermission):
    message = _("Sizda bu amalni bajarish uchun ruxsat yo‘q.")

    def __init__(self, model, pk):
        super().__init__()
        self.model = model
        self.pk = pk

    def __call__(self, *args, **kwargs):
        return self

    def has_permission(self, request, view):
        return self.model.objects.get(pk=self.pk).user == request.user
