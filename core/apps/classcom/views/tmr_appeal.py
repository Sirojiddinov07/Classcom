from django.db.models import Q
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from core.apps.classcom.choices import Role
from core.apps.classcom.models import TMRAppeal
from core.apps.classcom.serializers.tmr_appeal import TMRAppealSerializer
from core.apps.classcom.views import CustomPagination


class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == Role.MODERATOR


class TMRAppealAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsModerator]

    def get(self, request):
        user = request.user
        id = request.query_params.get("id")
        queryset = TMRAppeal.objects.filter(user=user)
        status = request.query_params.get("status")
        science = request.query_params.get("science")
        science_type = request.query_params.get("science_type")
        classes = request.query_params.get("classes")
        class_groups = request.query_params.get("class_groups")

        if id or status or science or science_type or classes or class_groups:
            filters = Q()
            if id:
                filters &= Q(id=id)
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
            serializer = TMRAppealSerializer(
                page, many=True, context={"request": request}
            )
            return paginator.get_paginated_response(serializer.data)
        serializer = TMRAppealSerializer(
            queryset, many=True, context={"request": request}
        )
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = TMRAppealSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
