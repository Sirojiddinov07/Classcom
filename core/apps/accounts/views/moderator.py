from django.utils import translation
from django.utils.translation import gettext as _
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.exceptions import NotAcceptable
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from core.http.models import User
from core.services import UserService
from ..serializers import ModeratorSerializer


class RegisterViewset(ViewSet):
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=["POST"], url_path="moderator")
    def register_moderator(self, request):
        """Moderator registratsiya qilish uchun api

        - science_types: fan turlari uchun example tanlov, majburiy, ...
        """

        phone = request.data.get("phone")
        if User.objects.filter(phone=phone).exists():
            raise NotAcceptable(
                {"detail": _("Phone number already registered")}
            )
        ser = ModeratorSerializer(
            data=request.data, context={"request": self.request}
        )
        ser.is_valid(raise_exception=True)
        ser.save()
        language = request.headers.get("Accept-Language", "uz")
        translation.activate(language)
        try:
            UserService().send_confirm(phone, language)
        except Exception as e:
            raise NotAcceptable(
                {"detail": str(e), "expired": str(e.kwargs.get("expired"))}
            )
        return Response({"detail": _("Tasdiqlash ko'di yuborildi")})
