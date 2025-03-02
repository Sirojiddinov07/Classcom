import typing
import uuid

from django.utils import translation
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema
from rest_framework import generics, permissions
from rest_framework import request as rest_request
from rest_framework import response, status, throttling, views, viewsets
from rest_framework.exceptions import NotAcceptable
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from core import enums, exceptions, services
from core.apps.accounts import models
from core.apps.accounts import serializers as sms_serializers
from core.apps.accounts.serializers.custom_token import (
    CustomTokenObtainPairSerializer,
)
from core.apps.classcom.models import Orders
from core.http import serializers
from core.http import views as http_views
from core.http.models import User


class RegisterView(views.APIView, services.UserService):
    """Register new user"""

    serializer_class = serializers.RegisterSerializer
    throttle_classes = [throttling.UserRateThrottle]
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        request=serializer_class,
        summary=_("Register new user"),
        description=_("Yangi user ro'yhatdan o'tish uchun"),
    )
    def post(self, request: rest_request.Request):
        ser = self.serializer_class(data=request.data)
        ser.is_valid(raise_exception=True)
        data = ser.data
        phone = data.get("phone")
        if User.objects.filter(phone=phone).exists():
            raise NotAcceptable(
                {"detail": _("Phone number already registered")}
            )
        # Create pending user
        user = self.create_user(
            phone,
            data.get("first_name"),
            data.get("last_name"),
            data.get("father_name"),
            request.data.get("password"),
            data.get("region"),
            data.get("district"),
            data.get("institution"),
            data.get("institution_number"),
            data.get("science"),
            data.get("role"),
            data.get("school_type"),
            data.get("class_group"),
        )
        language = request.headers.get("Accept-Language", "uz")
        translation.activate(language)
        self.send_confirmation(
            phone, language
        )  # Send confirmation code for sms eskiz.uz
        user.science_group.set(data.get("science_group"))
        Orders.objects.create(
            user=user,
            science_id=data.get("science"),
            class_type_id=data.get("class_group"),
        ).types.set(data.get("science_group"))
        return response.Response(
            {"detail": _(enums.Messages.SEND_MESSAGE) % {"phone": phone}},
            status=status.HTTP_202_ACCEPTED,
        )


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def get_serializer_context(self):
        return {"request": self.request}

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response(
                {"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class ConfirmView(views.APIView, services.UserService):
    """Confirm otp code"""

    serializer_class = serializers.ConfirmSerializer
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        request=serializer_class,
        summary=_("Confirm otp code."),
        description=_("Auth confirm."),
    )
    def post(self, request: rest_request.Request):
        ser = self.serializer_class(data=request.data)
        ser.is_valid(raise_exception=True)

        data = ser.data
        phone, code = data.get("phone"), data.get("code")

        try:
            # Check Sms confirmation otp code
            if services.SmsService.check_confirm(phone, code=code):
                # Create user
                token = self.validate_user(
                    User.objects.filter(phone=phone).first()
                )
                return response.Response(
                    data={
                        "detail": _(enums.Messages.OTP_CONFIRMED),
                        "token": token,
                    },
                    status=status.HTTP_202_ACCEPTED,
                )
        except exceptions.SmsException as e:
            return response.Response(
                {"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )  # Response exception for APIException
        except Exception as e:
            return response.Response(
                {"detail": e}, status=status.HTTP_400_BAD_REQUEST
            )  # Api exception for APIException


class ResetConfirmationCodeView(views.APIView, services.UserService):
    """Reset confirm otp code"""

    serializer_class = serializers.ResetConfirmationSerializer
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        request=serializer_class,
        summary="Reset confirm otp code.",
        description="Reset confirm otp code.",
    )
    def post(self, request: rest_request.Request):
        ser = self.serializer_class(data=request.data)
        ser.is_valid(raise_exception=True)

        data = ser.data
        code, phone = data.get("code"), data.get("phone")
        try:
            res = services.SmsService.check_confirm(phone, code)
            if res:
                token = models.ResetToken.objects.create(
                    user=User.objects.filter(phone=phone).first(),
                    token=str(uuid.uuid4()),
                )
                return response.Response(
                    data={
                        "token": token.token,
                        "created_at": token.created_at,
                        "updated_at": token.updated_at,
                    },
                    status=status.HTTP_200_OK,
                )
            return response.Response(
                data={"detail": _(enums.Messages.INVALID_OTP)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except exceptions.SmsException as e:
            return response.Response(
                {"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return response.Response(
                {"detail": e}, status=status.HTTP_400_BAD_REQUEST
            )


class ResetSetPasswordView(views.APIView, services.UserService):
    serializer_class = sms_serializers.SetPasswordSerializer
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        request=serializer_class,
        summary="Reset user password.",
        description="Reset user password.",
    )
    def post(self, request):
        ser = self.serializer_class(data=request.data)
        ser.is_valid(raise_exception=True)
        data = ser.data
        token = data.get("token")
        password = data.get("password")
        token = models.ResetToken.objects.filter(token=token)
        if not token.exists():
            return response.Response(
                {"detail": _("Token xato")},
                status=status.HTTP_400_BAD_REQUEST,
            )
        phone = token.first().user.phone
        token.delete()
        self.change_password(phone, password)
        return response.Response(
            {"detail": _("Parol yangilandi")}, status=status.HTTP_200_OK
        )


class ResendView(http_views.AbstractSendSms):
    """Resend Otp Code"""

    serializer_class = serializers.ResendSerializer


class ResetPasswordView(http_views.AbstractSendSms):
    """Reset user password"""

    serializer_class: typing.Type[serializers.ResetPasswordSerializer] = (
        serializers.ResetPasswordSerializer
    )


class MeView(viewsets.ViewSet):
    """Get user information"""

    serializer_class = serializers.UserDetailSerializer

    @extend_schema(
        request=serializer_class,
        summary="Get user information.",
        description="Get user information.",
    )
    def get(self, request: rest_request.Request):
        user = request.user
        return response.Response(
            serializers.UserDetailSerializer(
                user, context={"request": request}
            ).data
        )


class MeUpdateView(generics.UpdateAPIView):
    serializer_class = serializers.UserSerializer

    def get_object(self):
        return self.request.user
