import logging

from django.utils import timezone
from django.utils.translation import gettext as _
from rest_framework.decorators import action
from rest_framework.exceptions import APIException
from rest_framework.mixins import (
    RetrieveModelMixin,
    CreateModelMixin,
    ListModelMixin,
    DestroyModelMixin,
)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ViewSet

from .models import Orders, Payments
from .serializers import (
    OrderSerializer,
    PaymentCreateSerializer,
    UzumWebhookSerializer,
)
from .services import UzumService
from ..classcom.views import CustomPagination


class OrderViewSet(
    RetrieveModelMixin,
    ListModelMixin,
    CreateModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):
    serializer_class = OrderSerializer
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        user = self.request.user
        types = serializer.validated_data.get("types")
        current_date = timezone.now().date()

        if Orders.objects.filter(
            user=user,
            types__in=types,
            start_date__lte=current_date,
            end_date__gte=current_date,
            status=True,
        ).exists():
            raise APIException(
                _(
                    "Bu foydalanuvchi uchun bu turdagi buyurtma allaqachon mavjud."
                )
            )

        return serializer.save(user=user)

    def get_queryset(self):
        return Orders.objects.filter(user=self.request.user).order_by("-id")


class PaymentViewSet(ViewSet):
    serializer_class = PaymentCreateSerializer

    @action(detail=False, methods=["POST"], url_path="create")
    def create_payment(self, request):
        ser = self.serializer_class(data=request.data)
        ser.is_valid(raise_exception=True)
        data = ser.validated_data
        order = data.get("order")
        try:
            trans_id, redirect_url = UzumService().register(
                request.user.id,
                order.id,
                order.price,
                f"To'lov miqdori {order.price}, to'lov sanasi {order.created_at.strftime('%d-%m-%Y')}, "
                f"to'lov buyurtma raqami {order.id}, buyurtma {order.science}",
            )
        except Exception as e:
            raise APIException(str(e))
        Payments.objects.get_or_create(
            order=order, price=order.price, trans_id=trans_id
        )
        return Response(
            {
                "detail": _("Payment created"),
                "data": {"url": redirect_url},
            }
        )


class WebhookApiView(ViewSet):
    permission_classes = [AllowAny]

    @action(
        detail=False,
        methods=["POST", "GET"],
        url_name="uzum-webhook",
        url_path="uzum",
    )
    def uzum(self, request):
        ser = UzumWebhookSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        data = ser.data
        if data.get("operationState") != "SUCCESS":
            logging.error(ser.errors)
            return Response({"success": False})
        payment = Payments.objects.filter(trans_id=data.get("orderId"))
        if not payment.exists():
            logging.error("Order not found: {}".format(data.get("orderId")))
            return Response({"success": False})
        payment = payment.first()
        order = payment.order
        payment.status = True
        order.status = True
        payment.save()
        order.save()
        logging.debug("Payment success: {}".format(data.get("orderNumber")))
        return Response({"success": True})
