from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from ..serializers import ModeratorSerializer
from rest_framework.response import Response
from rest_framework import permissions
from django.utils.translation import gettext as _
from core.services import UserService
from rest_framework.exceptions import NotAcceptable


class RegisterViewset(ViewSet):

    serializer_class = ModeratorSerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['POST'], url_path="moderator")
    def register_moderator(self, request):
        """Moderator registratsiya qilish uchun api

            - science_types: fan turlari uchun example tanlov, majburiy, ...
        """
        ser = self.serializer_class(data=request.data)
        ser.is_valid(raise_exception=True)
        ser.save()
        phone = request.data.get("user").get("phone")
        try:
            UserService().send_confirm(phone)
        except Exception as e:
            raise NotAcceptable({
                "detail": str(e),
                "expired": str(e.kwargs.get("expired"))
            })
        return Response({"detail": _("Tasdiqlash ko'di yuborildi")})
