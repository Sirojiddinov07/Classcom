from rest_framework import generics

from core.apps.classcom.models.chat import Chat
from core.apps.classcom.serializers.chat import ChatSerializer
from rest_framework import permissions


class ChatListCreateView(generics.ListCreateAPIView):
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Chat.objects.filter(user=user).order_by('time')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
