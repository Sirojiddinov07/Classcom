"""
Search view
"""
from rest_framework import views
from rest_framework import response

from core.apps.classcom import models
from core.apps.classcom import serializers
from django.db.models import Q


class UnifiedSearchView(views.APIView):
    def get(self, request, *args, **kwargs):
        serializer = serializers.SearchSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        query = serializer.validated_data.get("query", "")

        # Searching Plans
        plan_results = models.Plan.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query)
        )
        plan_serializer = serializers.PlanSerializer(plan_results, many=True)

        # Searching Schedules
        user = request.user
        schedule_results = models.Schedule.objects.filter(
            Q(shift__icontains=query) |
            Q(weekday__icontains=query) |
            Q(lesson_time__icontains=query),
            user=user
        )
        schedule_serializer = serializers.ScheduleListSerializer(
            schedule_results, many=True
        )

        # Searching Resources
        resource_results = models.Resource.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query)
        )
        resource_serializer = serializers.ResourceSerializer(
            resource_results, many=True
        )

        results = {
            "plans": plan_serializer.data,
            "schedules": schedule_serializer.data,
            "resources": resource_serializer.data,
        }

        return response.Response(results)
