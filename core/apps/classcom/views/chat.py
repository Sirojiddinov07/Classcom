from rest_framework import generics, permissions

from core.apps.classcom.models.chat import Chat
from core.apps.classcom.serializers.chat import ChatSerializer


class ChatListCreateView(generics.ListCreateAPIView):
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        user = self.request.user
        return Chat.objects.filter(user=user).order_by("-time")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
