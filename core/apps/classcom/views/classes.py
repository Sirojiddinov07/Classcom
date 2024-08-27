from django.utils.translation import gettext_lazy as _
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.apps.classcom import models, serializers
from core.apps.classcom.choices import Role
from core.apps.classcom.views.region import CustomPagination


class ClassesViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows classes to be viewed or edited.
    """

    permission_classes = [AllowAny]
    queryset = models.Classes.objects.all()
    serializer_class = serializers.ClassesSerializer
    pagination_class = CustomPagination


class ClassTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows class types to be viewed or edited.
    """

    permission_classes = [AllowAny]
    queryset = models.ClassType.objects.all()
    serializer_class = serializers.ClassTypeSerializer
    pagination_class = CustomPagination


############################################################################################################
# Moderaor permissions bolgan classlar
############################################################################################################
class ModeratorClassesApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if user.role == Role.MODERATOR:
            moderator = models.Moderator.objects.filter(user=user).first()
            if moderator:
                classes = moderator.classes.all()
                serializer = serializers.ClassesSerializer(classes, many=True)
                return Response(serializer.data)
            else:
                raise PermissionDenied(_("Moderator topilmadi."))
        else:
            raise PermissionDenied(
                _("Sizda bu amalni bajarish uchun ruxsat yo‘q.")
            )
