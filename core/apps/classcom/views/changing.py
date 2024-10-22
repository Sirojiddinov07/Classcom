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
from core.apps.classcom.serializers import (
    ChangeModeratorSerializer,
    ChangeModeratorDetailSerializer,
)
from core.apps.classcom.views import CustomPagination


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
            paginator = CustomPagination()
            page = paginator.paginate_queryset(queryset, request)
            if page is not None:
                serializer = ChangeModeratorDetailSerializer(page, many=True)
                return paginator.get_paginated_response(serializer.data)
            serializer = ChangeModeratorDetailSerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response(
                {"error": "Siz moderator emassiz!"},
                status=status.HTTP_400_BAD_REQUEST,
            )
