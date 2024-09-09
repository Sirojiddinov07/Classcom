from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import OrderViewSet, PaymentViewSet, WebhookApiView

router = DefaultRouter()
router.register("orders", OrderViewSet, basename="order")
router.register("payment", PaymentViewSet, basename="payment")
router.register("webkook", WebhookApiView, basename="webhook")

urlpatterns = [path("", include(router.urls))]
