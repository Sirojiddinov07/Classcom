"""
Search view
"""
from rest_framework import views
from rest_framework import response

from core.apps.classcom import models
from core.apps.classcom import serializers


class UnifiedSearchView(views.APIView):
    def get(self, request, *args, **kwargs):
        serializer = serializers.SearchSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        query = serializer.validated_data.get('query', '')

        plan_results = models.Plan.objects.filter(
            name__icontains=query
        ) | models.Plan.objects.filter(
            description__icontains=query
        )
        plan_serializer = serializers.PlanSerializer(plan_results, many=True)

        schedule_results = models.Schedule.objects.filter(
            shift__icontains=query
        ) | models.Schedule.objects.filter(
            weekday__icontains=query
        ) | models.Schedule.objects.filter(
            lesson_time__icontains=query
        )
        schedule_serializer = serializers.ScheduleListSerializer(schedule_results, many=True)

        resource_results = models.Resource.objects.filter(
            name__icontains=query
        ) | models.Resource.objects.filter(
            description__icontains=query
        )
        resource_serializer = serializers.ResourceSerializer(resource_results, many=True)

        results = {
            'plans': plan_serializer.data,
            'schedules': schedule_serializer.data,
            'resources': resource_serializer.data
        }

        return response.Response(results)
