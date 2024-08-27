from django.utils.translation import gettext_lazy as _
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.apps.classcom.choices import Role
from core.apps.classcom.models import Quarter, Moderator
from core.apps.classcom.serializers import QuarterMiniSerializer


class QuarterListView(generics.ListAPIView):
    queryset = Quarter.objects.all().order_by("choices")
    serializer_class = QuarterMiniSerializer


############################################################################################################
# Moderaor permissions bor bolgan choraklar uchun
############################################################################################################
class ModeratorQuarterApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if user.role == Role.MODERATOR:
            moderator = Moderator.objects.filter(user=user).first()
            if moderator:
                quarters = moderator.quarters.all()
                serializer = QuarterMiniSerializer(quarters, many=True)
                return Response(serializer.data)
            else:
                raise PermissionDenied(_("Moderator topilmadi."))
        else:
            raise PermissionDenied(
                _("Sizda bu amalni bajarish uchun ruxsat yo‘q.")
            )
