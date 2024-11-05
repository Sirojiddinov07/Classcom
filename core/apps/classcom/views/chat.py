from rest_framework import generics, permissions
from rest_framework import status
from rest_framework.response import Response

from core.apps.classcom.models.chat import Chat
from core.apps.classcom.serializers.chat import ChatSerializer


class ChatListCreateView(generics.ListCreateAPIView, generics.UpdateAPIView):
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        user = self.request.user
        return Chat.objects.filter(user=user).order_by("-time")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def patch(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)
