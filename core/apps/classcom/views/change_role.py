from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from core.apps.classcom.models import Moderator
from core.apps.classcom.serializers.change_role import ChangeRoleSerializer


class ChangeRoleView(generics.CreateAPIView):
    queryset = Moderator.objects.all()
    serializer_class = ChangeRoleSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()
