from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import never_cache
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.apps.classcom import models, serializers
from . import CustomPagination
from ..choices import Role
from ..filters import ResourceFilter


class ResourceTypesViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=["GET"], url_path="resource-types")
    def get(self, request):
        """
        Resource Turlarini olish uchun GET request
        """
        resource_types = models.ResourceType.objects.all()
        serializer = serializers.ResourceTypeSerializer(
            resource_types, many=True
        )
        return Response(serializer.data)


class ResourceViewSet(viewsets.ModelViewSet):
    queryset = models.Resource.objects.all().order_by("order_number")
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ResourceFilter
    pagination_class = CustomPagination

    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def perform_create(self, serializer):
        user = self.request.user
        resource_type = serializer.validated_data.get("type")

        if user.role == Role.MODERATOR:
            moderator = models.Moderator.objects.filter(user=user).first()
            if (
                moderator
                and moderator.resource_type.filter(
                    id=resource_type.id
                ).exists()
            ):
                serializer.save(user=user)
            else:
                raise PermissionDenied(
                    _("Sizda bu amalni bajarish uchun ruxsat yo‘q.")
                )
        else:
            raise PermissionDenied(
                _("Sizda bu amalni bajarish uchun ruxsat yo‘q.")
            )

    def get_serializer_class(self):
        match self.action:
            case "create" | "update" | "partial_update":
                return serializers.ResourceCreateSerializer
            case "retrieve":
                return serializers.ResourceDetailSerializer
        return serializers.ResourceSerializer


############################################################################################################
# Moderator Resource Types
############################################################################################################
class ModeratorResourceTypesAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if user.role == Role.MODERATOR:
            moderator = models.Moderator.objects.filter(user=user).first()
            if moderator:
                resource_types = moderator.resource_type.all()
                serializer = serializers.ResourceTypeSerializer(
                    resource_types, many=True
                )
                return Response(serializer.data)
            else:
                raise PermissionDenied(_("Moderator topilmadi."))
        else:
            raise PermissionDenied(
                _("Sizda bu amalni bajarish uchun ruxsat yo‘q.")
            )
