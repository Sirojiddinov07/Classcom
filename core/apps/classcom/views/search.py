import logging

from django.core.cache import cache
from django.db.models import Q
from rest_framework import views
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.apps.classcom import models
from core.apps.classcom import serializers

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class UnifiedSearchPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class UnifiedSearchView(views.APIView):
    pagination_class = UnifiedSearchPagination
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        serializer = serializers.SearchSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        query = serializer.validated_data.get("query", "")

        logger.debug(f"Received search query: {query}")

        if not query:
            return Response({"resources": [], "plans": [], "schedules": []})

        cache_key = f"search_results_{query}"
        cached_results = cache.get(cache_key)

        if cached_results:
            return Response(cached_results)

        query_words = query.split()
        resource_query = Q()
        plan_query = Q()
        schedule_query = Q()

        for word in query_words:
            resource_query &= (
                Q(name__icontains=word)
                | Q(description__icontains=word)
                | Q(type__name__icontains=word)
                | Q(classes__name__icontains=word)
                | Q(user__first_name__icontains=word)
                | Q(user__last_name__icontains=word)
                | Q(name_ru__icontains=word)
                | Q(description_ru__icontains=word)
                | Q(type__name_ru__icontains=word)
                | Q(classes__name_ru__icontains=word)
                | Q(name_uz__icontains=word)
                | Q(description_uz__icontains=word)
                | Q(type__name_uz__icontains=word)
                | Q(classes__name_uz__icontains=word)
            )
            plan_query &= (
                Q(name__icontains=word)
                | Q(description__icontains=word)
                | Q(user__first_name__icontains=word)
                | Q(user__last_name__icontains=word)
                | Q(name_ru__icontains=word)
                | Q(description_ru__icontains=word)
                | Q(name_uz__icontains=word)
                | Q(description_uz__icontains=word)
            )
            schedule_query &= (
                Q(science__name__icontains=word)
                | Q(classes__name__icontains=word)
                | Q(user__first_name__icontains=word)
                | Q(user__last_name__icontains=word)
                | Q(science__name_ru__icontains=word)
                | Q(classes__name_ru__icontains=word)
                | Q(science__name_uz__icontains=word)
                | Q(classes__name_uz__icontains=word)
            )

        resource_results = (
            models.Resource.objects.filter(resource_query)
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

        logger.debug(f"Resource SQL Query: {resource_results.query}")

        plan_results = (
            models.Plan.objects.filter(plan_query)
            .select_related("user")
            .only("name", "description", "user__first_name", "user__last_name")
        )

        logger.debug(f"Plan SQL Query: {plan_results.query}")

        schedule_results = (
            models.Schedule.objects.filter(schedule_query)
            .select_related("user")
            .only(
                "science__name",
                "classes__name",
                "user__first_name",
                "user__last_name",
            )
        )

        logger.debug(f"Schedule SQL Query: {schedule_results.query}")

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
