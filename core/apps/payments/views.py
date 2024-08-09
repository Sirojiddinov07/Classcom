from rest_framework.viewsets import GenericViewSet, ViewSet
from rest_framework.mixins import (
    RetrieveModelMixin,
    CreateModelMixin,
    ListModelMixin,
    DestroyModelMixin
)
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Orders, Payments
from uuid import uuid4
from .serializers import OrderSerializer, PaymentCreateSerializer
from django.utils.translation import gettext as _


class OrderViewSet(
    RetrieveModelMixin, ListModelMixin, CreateModelMixin, DestroyModelMixin, GenericViewSet
):
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    def get_queryset(self):
        return Orders.objects.filter(user=self.request.user)


class PaymentViewSet(ViewSet):
    serializer_class = PaymentCreateSerializer

    @action(detail=False, methods=['POST'], url_path="create")
    def create_payment(self, request):
        ser = self.serializer_class(data=request.data)
        ser.is_valid(raise_exception=True)
        data = ser.validated_data
        order = data.get("order")
        payment = Payments.objects.create(
            order=order,
            price=order.price,
            trans_id=str(uuid4())
        )
        return Response({
            "detail": _("Payment created"),
            "data": {
                "url": "https://uzumbank.uz/payment/{}".format(payment.trans_id)
            }
        })
