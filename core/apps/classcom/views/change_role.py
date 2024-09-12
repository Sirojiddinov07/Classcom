from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.apps.classcom.models import Moderator
from core.apps.classcom.serializers.change_role import ChangeRoleSerializer


class ChangeRoleView(generics.CreateAPIView):
    queryset = Moderator.objects.all()
    serializer_class = ChangeRoleSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = ChangeRoleSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
