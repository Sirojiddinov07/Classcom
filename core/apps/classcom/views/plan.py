from rest_framework import viewsets, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from core.apps.classcom import models
from core.apps.classcom import serializers
from core.http.serializers import UserSerializer


class PlanViewSet(viewsets.ModelViewSet):
    queryset = models.Plan.objects.all().order_by("id")
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["classes", "topic", "hour", "quarter"]
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.request.method == "GET":
            if self.action == "retrieve":
                return serializers.PlanDetailSerializer
            return serializers.PlanSerializer
        return serializers.PlanCreateSerializer

    @action(detail=False, methods=["post"], url_path='filter-resources')
    def filter_resources(self, request):
        science_id = request.data.get('science')
        classes_id = request.data.get('classes')

        if not science_id or not classes_id:
            return Response({"detail": "science and classes fields are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Filter the plans based on science and classes
        plans = models.Plan.objects.filter(science_id=science_id, classes_id=classes_id)

        # Get the plan_resource items and their creators
        plan_resources = models.Media.objects.filter(plan__in=plans).distinct()
        creators = models.User.objects.filter(plan__in=plans).distinct()

        # Serialize the results
        resource_serializer = serializers.MediaSerializer(plan_resources, many=True)
        creator_serializer = UserSerializer(creators, many=True)

        return Response({
            'plan_resources': resource_serializer.data,
            'creators': creator_serializer.data
        })