from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
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

            status = request.query_params.get("status")
            science = request.query_params.get("science")
            science_type = request.query_params.get("science_type")
            classes = request.query_params.get("classes")
            class_groups = request.query_params.get("class_groups")

            if status or science or science_type or classes or class_groups:
                filters = Q()
                if status:
                    filters &= Q(status=status)
                if science:
                    filters &= Q(science=science)
                if science_type:
                    filters &= Q(science_type__id=science_type)
                if classes:
                    filters &= Q(classes=classes)
                if class_groups:
                    filters &= Q(class_groups=class_groups)
                queryset = queryset.filter(filters)

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
                status=HTTP_400_BAD_REQUEST,
            )
