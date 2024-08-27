from django.utils.translation import gettext_lazy as _
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.apps.classcom.choices import Role
from core.apps.classcom.models import Moderator
from core.http.models import ClassGroup
from core.http.serializers import ClassGroupSerializer


class FilteredSchoolGroupViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = ClassGroupSerializer
    http_method_names = ["get"]

    def get_queryset(self):
        queryset = ClassGroup.objects.all()

        return queryset


############################################################################################################
# # Moderator permissions bor bolgan classlar
############################################################################################################
class ModeratorClassGroupApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if user.role == Role.MODERATOR:
            moderator = Moderator.objects.filter(user=user).first()
            if moderator:
                class_group = moderator.class_group.all()
                serializer = ClassGroupSerializer(class_group, many=True)
                return Response(serializer.data)
            else:
                raise PermissionDenied(_("Moderator topilmadi."))
        else:
            raise PermissionDenied(
                _("Sizda bu amalni bajarish uchun ruxsat yo‘q.")
            )
