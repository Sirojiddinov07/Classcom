from django.utils.translation import gettext_lazy as _
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone

from core.apps.classcom.choices import Role
from core.apps.classcom.models import Moderator
from core.apps.payments.models import Orders
from core.http.models import ClassGroup
from core.http.serializers import ClassGroupSerializer


class FilteredSchoolGroupViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = ClassGroupSerializer
    http_method_names = ["get"]

    def get_queryset(self):
        user = self.request.user
        queryset = ClassGroup.objects.all()
        current_date = timezone.now().date()

        if user.is_authenticated and user.role == Role.USER:
            orders = Orders.objects.filter(
                user=user,
                status=True,
                start_date__lte=current_date,
                end_date__gte=current_date,
            )
            queryset = queryset.filter(orders__in=orders)

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
                class_group = moderator.class_groups.all()
                serializer = ClassGroupSerializer(class_group, many=True)
                return Response(serializer.data)
            else:
                raise PermissionDenied(_("Moderator topilmadi."))
        else:
            raise PermissionDenied(
                _("Sizda bu amalni bajarish uchun ruxsat yo‘q.")
            )
