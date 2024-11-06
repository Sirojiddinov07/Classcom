from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from core.apps.classcom.models.chat import Chat
from core.apps.classcom.serializers.chat import ChatSerializer


class ChatView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None
    serializer_class = ChatSerializer

    def get(self, request):
        id = request.query_params.get("id")
        user = request.user
        if id:
            try:
                chat = Chat.objects.get(user=user, id=id)
                serializer = self.serializer_class(chat)
                return Response(serializer.data)
            except Chat.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            chats = Chat.objects.filter(user=user).order_by("-time")
            serializer = self.serializer_class(chats, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        id = request.query_params.get("id")
        try:
            chat = Chat.objects.get(user=request.user, id=id)
        except Chat.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(
            chat, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save(is_read=True)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
