import logging

from rest_framework import viewsets, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from core.apps.classcom import models
from core.apps.classcom import serializers
from core.http.serializers import UserSerializer

logger = logging.getLogger(__name__)


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



    @action(detail=False, methods=["post"], url_path="filter-resources")
    def filter_resources(self, request):
        science_id = request.data.get("science")
        classes_id = request.data.get("classes")

        if not science_id or not classes_id:
            return Response(
                {"detail": "science and classes fields are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Filter the plans based on science and classes
        plans = models.Plan.objects.filter(
            science_id=science_id, classes_id=classes_id
        )

        # Get the plan_resource items and their creators
        plan_resources = models.Media.objects.filter(plan__in=plans).distinct()
        creators = models.User.objects.filter(plan__in=plans).distinct()

        # Serialize the results
        resource_serializer = serializers.MediaSerializer(
            plan_resources, many=True
        )
        creator_serializer = UserSerializer(creators, many=True)

        return Response(
            {
                "plan_resources": resource_serializer.data,
                "creators": creator_serializer.data,
            }
        )


    @action(detail=False, methods=["get"], url_path="grouped-plans")
    def grouped_plans(self, request):
        grouped_plans = models.Plan.get_grouped_plans()
        grouped_data = []
        for classes, quarter, science, plans in grouped_plans:
            plan_serializer = serializers.PlanDetailSerializerForGroupped(plans, many=True, context={'request': request})
            grouped_data.append({
                "classes": {
                    "id": classes.id,
                },
                "quarter": {
                    "id": quarter.id,
                },
                "science": {
                    "id": science.id,
                },
                "plans": plan_serializer.data
            })
        return Response(grouped_data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user != request.user:
            return Response("you can not delete")
        self.perform_destroy(instance)
        logger.info(
            f"Plan with id {instance.id} deleted successfully by user {request.user}"
        )
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()
