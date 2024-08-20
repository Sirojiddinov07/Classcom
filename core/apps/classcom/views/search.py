from django.core.cache import cache
from django.db.models import Q
from rest_framework import views
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from core.apps.classcom import models
from core.apps.classcom import serializers


class UnifiedSearchPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class UnifiedSearchView(views.APIView):
    pagination_class = UnifiedSearchPagination

    def get(self, request, *args, **kwargs):
        serializer = serializers.SearchSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        query = serializer.validated_data.get("query", "")

        cache_key = f"search_results_{query}"
        cached_results = cache.get(cache_key)

        if cached_results:
            return Response(cached_results)

        resource_results = (
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
            .only(
                "name",
                "description",
                "type__name",
                "user__first_name",
                "user__last_name",
            )
        )

        plan_results = (
            models.Plan.objects.filter(
                Q(name__icontains=query)
                | Q(description__icontains=query)
                | Q(user__first_name__icontains=query)
                | Q(user__last_name__icontains=query)
            )
            .select_related("user")
            .only("name", "description", "user__first_name", "user__last_name")
        )

        schedule_results = (
            models.Schedule.objects.filter(
                Q(science__name__icontains=query)
                | Q(user__first_name__icontains=query)
                | Q(user__last_name__icontains=query)
            )
            .select_related("user")
            .only("science__name", "user__first_name", "user__last_name")
        )

        resource_serializer = serializers.ResourceSerializer(
            resource_results, many=True, context={"request": request}
        )
        plan_serializer = serializers.PlanSerializer(
            plan_results, many=True, context={"request": request}
        )
        schedule_serializer = serializers.ScheduleListSerializer(
            schedule_results, many=True, context={"request": request}
        )

        results = {
            "resources": resource_serializer.data,
            "plans": plan_serializer.data,
            "schedules": schedule_serializer.data,
        }

        cache.set(cache_key, results, timeout=60 * 15)

        return Response(results)
