from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from core.apps.websocket.models import Notification
from core.apps.websocket.serializers.notification import NotificationSerializer


class NotificationViewSet(ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user, is_read=False)
