from rest_framework.viewsets import GenericViewSet, ViewSet
from rest_framework.mixins import (
    RetrieveModelMixin,
    CreateModelMixin,
    ListModelMixin,
    DestroyModelMixin
)
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Orders
from .serializers import OrderSerializer


class OrderViewSet(
    RetrieveModelMixin, ListModelMixin, CreateModelMixin, DestroyModelMixin, GenericViewSet
):
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    def get_queryset(self):
        return Orders.objects.filter(user=self.request.user)


class PaymentViewSet(ViewSet):

    @action(detail=False, methods=['POST'], url_path="create-payment")
    def create_payment(self, request):
        return Response({
            "success": True
        })