import logging

from rest_framework import viewsets, status, serializers as rsr
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from core.apps.classcom import models, serializers, services
from core.http.serializers import UserSerializer
from django.utils.translation import gettext as _
from drf_spectacular.utils import (
    extend_schema,
    inline_serializer,
)

logger = logging.getLogger(__name__)


class PlanViewSet(viewsets.ModelViewSet):
    queryset = models.Plan.objects.all().order_by("id")
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["classes", "topic", "hour", "quarter"]
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        match self.action:
            case "create" | "update" | "partial_update":
                return serializers.PlanCreateSerializer
            case "retrieve":
                return serializers.PlanDetailSerializer
            case "set_media":
                return serializers.PlanSetMediaSerializer
            case _:
                return serializers.PlanSerializer

    @extend_schema(
        responses={
            200: inline_serializer(
                name="PlanMediaSerializer",
                fields={"detail": rsr.CharField()},
            )
        },
    )
    @action(detail=True, methods=["POSt"], url_path="set-media")
    def set_media(self, request, pk):
        ser = self.get_serializer_class()(data=request.data)
        ser.is_valid(raise_exception=True)
        obj = self.get_queryset().filter(id=pk)
        if not obj.exists():
            return Response(
                data={"detail": _("Plan not found")},
                status=status.HTTP_404_NOT_FOUND,
            )
        obj = obj.first()
        validated_data = ser.validated_data

        media = validated_data.pop("media", [])
        names = validated_data.pop("names", [])
        descriptions = validated_data.pop("descriptions", [])
        service = services.BaseService()

        for index, media_item in enumerate(media):
            media = models.Media.objects.create(
                file=media_item,
                name=service.list_index_default(names, index),
                desc=service.list_index_default(descriptions, index),
            )
            obj.plan_resource.add(media)

        return Response(
            data={"detail": _("Media files uploaded")},
            status=status.HTTP_201_CREATED,
        )

    @action(detail=False, methods=["post"], url_path="filter-resources")
    def filter_resources(self, request):
        science_id = request.data.get("science")
        classes_id = request.data.get("classes")

        if not science_id or not classes_id:
            return Response(
                {"detail": "science and classes fields are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        plans = models.Plan.objects.filter(
            science_id=science_id, classes_id=classes_id
        )

        plan_resources = models.Media.objects.filter(plan__in=plans).distinct()
        creators = models.User.objects.filter(plan__in=plans).distinct()

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

    @action(detail=True, methods=["get"], url_path="related-plans")
    def related_plans(self, request, pk=None):
        try:
            instance = models.Plan.objects.get(pk=pk)
        except models.Plan.DoesNotExist:
            raise NotFound("Plan not found")
        related_plans = models.Plan.objects.filter(
            classes=instance.classes,
            quarter=instance.quarter,
            science=instance.science,
        ).order_by("id")

        topics = [{"id": plan.id, "topic_id": plan.topic.id, "name": plan.topic.name, "hour": plan.hour} for plan in related_plans]

        grouped_data = {
            "classes": instance.classes.name,
            "quarter": instance.quarter.choices,
            "science": instance.science.name,
            "topics": topics,
        }

        return Response(grouped_data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user != request.user:
            return Response(
                "you can not delete", status=status.HTTP_403_FORBIDDEN
            )
        self.perform_destroy(instance)
        logger.info(
            f"Plan with id {instance.id} deleted successfully by\
                  user {request.user}"
        )
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()
