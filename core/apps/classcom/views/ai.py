from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from core.apps.classcom.choices import Role
from core.apps.classcom.models import Ai
from core.apps.classcom.serializers import AiSerializer


class AiViewSet(ModelViewSet):
    serializer_class = AiSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = Ai.objects.all()
        topic = self.request.query_params.get("topic", None)
        if topic is not None:
            queryset = queryset.filter(topic=topic)
        return queryset

    def perform_create(self, serializer):
        if not self.request.user.role == Role.MODERATOR:
            raise PermissionDenied(
                _("Sizda buni amalga oshirishga ruxsat yo'q.")
            )
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        instance = self.get_object()
        if instance.user != self.request.user:
            raise PermissionDenied(
                _("Sizda buni amalga oshirishga ruxsat yo'q.")
            )
        serializer.save()
