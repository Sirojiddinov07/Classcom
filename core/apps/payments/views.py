from django.utils.translation import gettext as _
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.mixins import (
    RetrieveModelMixin,
    CreateModelMixin,
    ListModelMixin,
    DestroyModelMixin,
)

from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ViewSet
from rest_framework.exceptions import APIException

from .models import Orders, Payments
from .serializers import OrderSerializer, PaymentCreateSerializer
from .services import UzumService


class OrderViewSet(
    RetrieveModelMixin,
    ListModelMixin,
    CreateModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    def get_queryset(self):
        return Orders.objects.filter(user=self.request.user)


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
                request.user.id, order.id, order.price, "1 chorak uchun to'lov"
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
        print(request.GET)
        return Response({"success": True})
