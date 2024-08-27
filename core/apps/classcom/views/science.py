from django.utils.translation import gettext_lazy as _
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.apps.classcom import models, serializers
from core.apps.classcom.choices import Role


class ScienceViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    queryset = models.Science.objects.all().order_by("order_number")
    serializer_class = serializers.ScienceSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["science_grp", "name"]

    def get_queryset(self):
        queryset = models.Science.objects.all()
        class_group = self.request.query_params.get("class_group", None)
        if class_group is not None:
            queryset = queryset.filter(class_group=class_group)
        return queryset


class ScienceTypesViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = serializers.ScienceTypesSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["name"]
    http_method_names = ["get"]

    def get_queryset(self):
        queryset = models.ScienceTypes.objects.all()
        science_id = self.request.query_params.get("science", None)
        class_group = self.request.query_params.get("class_group", None)
        if science_id is not None:
            queryset = queryset.filter(science__id=science_id)
        if class_group is not None:
            queryset = queryset.filter(science__class_group=class_group)
        return queryset


############################################################################################################
# Moderator permissions bor bolgan fanlar uchun
############################################################################################################
class ModeratorScienceApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if user.role == Role.MODERATOR:
            moderator = models.Moderator.objects.filter(user=user).first()
            if moderator:
                sciences = moderator.science.all()
                serializer = serializers.ScienceSerializer(sciences, many=True)
                return Response(serializer.data)
            else:
                raise PermissionDenied(_("Moderator topilmadi."))
        else:
            raise PermissionDenied(
                _("Sizda bu amalni bajarish uchun ruxsat yo‘q.")
            )


class ModeratorScienceTypeApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if user.role == Role.MODERATOR:
            moderator = models.Moderator.objects.filter(user=user).first()
            if moderator:
                science_type = moderator.science_type.all()
                science_id = self.request.query_params.get("science", None)
                class_group = self.request.query_params.get(
                    "class_group", None
                )

                if science_id is not None:
                    science_type = science_type.filter(science__id=science_id)
                if class_group is not None:
                    science_type = science_type.filter(
                        science__class_group=class_group
                    )

                serializer = serializers.ScienceTypesSerializer(
                    science_type, many=True
                )
                return Response(serializer.data)
            else:
                raise PermissionDenied(_("Moderator topilmadi."))
        else:
            raise PermissionDenied(
                _("Sizda bu amalni bajarish uchun ruxsat yo‘q.")
            )
