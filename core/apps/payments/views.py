from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    RetrieveModelMixin,
    CreateModelMixin,
    ListModelMixin,
    DestroyModelMixin
)
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
