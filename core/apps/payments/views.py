from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    RetrieveModelMixin,
    CreateModelMixin,
    ListModelMixin,
)
from .models import Orders
from .serializers import OrderSerializer


class OrderViewSet(
    RetrieveModelMixin, ListModelMixin, CreateModelMixin, GenericViewSet
):
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Orders.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)