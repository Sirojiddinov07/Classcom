from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.apps.classcom.models import (
    ChangeModeratorStatus,
    ChangeModerator,
    Moderator,
)
from core.apps.classcom.serializers import ChangeModeratorSerializer


class ChangeModeratorAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        if (
            user.role == "moderator"
            and Moderator.objects.filter(user=user).exists()
        ):

            if ChangeModerator.objects.filter(
                user=user, status=ChangeModeratorStatus.PENDING
            ).exists():
                return Response(
                    {"error": _("Siz allaqachon ariza topshirgansiz")},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            serializer = ChangeModeratorSerializer(
                data=request.data, context={"request": request}
            )
            if serializer.is_valid():
                serializer.save()
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED
                )
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        else:
            return Response(
                {"error": "Siz moderator meassiz!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def get(self, request):
        user = request.user
        if user.role == "moderator":
            queryset = ChangeModerator.objects.filter(user=user)
            serializer = ChangeModeratorSerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response(
                {"error": "Siz moderator emassiz!"},
                status=status.HTTP_400_BAD_REQUEST,
            )
