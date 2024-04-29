from rest_framework import viewsets

from ..serializers.notification import NotificationSerializer
from ..models.notification import Notification


class NotificationListView(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
