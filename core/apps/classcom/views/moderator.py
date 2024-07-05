from rest_framework import status, views
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from core.apps.classcom.models import Moderator
from core.apps.classcom.serializers import ModeratorCreateSerializer


class ModeratorCreateViewSet(views.APIView):
    permission_classes = [AllowAny]
    serializer_class = ModeratorCreateSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        moderators = Moderator.objects.filter(user=request.user)
        serializer = self.serializer_class(moderators, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)