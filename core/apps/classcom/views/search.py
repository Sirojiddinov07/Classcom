"""
Search view
"""

from django.db.models import Q
from rest_framework import response
from rest_framework import views

from core.apps.classcom import models
from core.apps.classcom import serializers


class UnifiedSearchView(views.APIView):
    def get(self, request, *args, **kwargs):
        serializer = serializers.SearchSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        query = serializer.validated_data.get("query", "")

        # Searching Resources
        resource_results = models.Resource.objects.filter(
            Q(name__icontains=query)
            | Q(description__icontains=query)
            | Q(type__name__icontains=query)
            | Q(classes__name__icontains=query)
            | Q(user__first_name__icontains=query)
            | Q(user__last_name__icontains=query)
        )
        resource_serializer = serializers.ResourceSerializer(
            resource_results, many=True, context={"request": request}
        )

        results = {
            "resources": resource_serializer.data,
        }

        return response.Response(results)
