from asgiref.sync import sync_to_async
from django.core.cache import cache
from django.db.models import Q
from rest_framework import views
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from core.apps.classcom import models
from core.apps.classcom import serializers
from core.apps.classcom.serializers import (
    ScheduleListSerializer,
    PlanSerializer,
    ResourceSerializer,
)


class UnifiedSearchPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class UnifiedSearchView(views.APIView):
    pagination_class = UnifiedSearchPagination

    async def get(self, request, *args, **kwargs):
        serializer = serializers.SearchSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        query = await sync_to_async(serializer.validated_data.get)("query", "")

        cache_key = f"search_results_{query}"
        cached_results = cache.get(cache_key)

        if cached_results:
            return Response(cached_results)

        resource_results = await sync_to_async(list)(
            models.Resource.objects.filter(
                Q(name__icontains=query)
                | Q(description__icontains=query)
                | Q(type__name__icontains=query)
                | Q(classes__name__icontains=query)
                | Q(user__first_name__icontains=query)
                | Q(user__last_name__icontains=query)
            )
            .select_related("type", "user")
            .prefetch_related("classes")
        )
        resource_serializer = ResourceSerializer(
            resource_results, many=True, context={"request": request}
        )

        plan_results = await sync_to_async(list)(
            models.Plan.objects.filter(
                Q(name__icontains=query)
                | Q(description__icontains=query)
                | Q(user__first_name__icontains=query)
                | Q(user__last_name__icontains=query)
            ).select_related("user")
        )
        plan_serializer = PlanSerializer(
            plan_results, many=True, context={"request": request}
        )

        schedule_results = await sync_to_async(list)(
            models.Schedule.objects.filter(
                Q(name__icontains=query)
                | Q(description__icontains=query)
                | Q(user__first_name__icontains=query)
                | Q(user__last_name__icontains=query)
            ).select_related("user")
        )
        schedule_serializer = ScheduleListSerializer(
            schedule_results, many=True, context={"request": request}
        )

        results = {
            "resources": resource_serializer.data,
            "plans": plan_serializer.data,
            "schedules": schedule_serializer.data,
        }

        cache.set(cache_key, results, timeout=60 * 15)

        return Response(results)
