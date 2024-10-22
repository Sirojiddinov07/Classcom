from django.db.models import Q
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.apps.classcom.models import PlanAppeal
from core.apps.classcom.serializers.rtm_appeal import PlanAppealSerializer
from core.apps.classcom.views import CustomPagination


class PlanAppealView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = PlanAppealSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            try:
                instance = serializer.save()
                return Response(
                    PlanAppealSerializer(instance).data,
                    status=status.HTTP_201_CREATED,
                )
            except Exception as e:
                return Response(
                    {"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        queryset = PlanAppeal.objects.filter(user=request.user)

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
            serializer = PlanAppealSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        serializer = PlanAppealSerializer(queryset, many=True)
        return Response(serializer.data)
