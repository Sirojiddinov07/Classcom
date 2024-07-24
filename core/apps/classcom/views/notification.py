from rest_framework import viewsets

from ..models.notification import Notification
from ..serializers.notification import NotificationSerializer


class NotificationListView(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
