from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, decorators, exceptions
from rest_framework.response import Response
from core.apps.classcom import services
from datetime import datetime

from core.apps.classcom import models, serializers
from drf_spectacular.utils import extend_schema, OpenApiParameter


class TopicViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Topic.objects.all()
    serializer_class = serializers.TopicSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['_class', 'quarter', 'science']

    def get_permissions(self):
        perms = []
        match self.action:
            case "get_topic":
                perms.append(permissions.IsAuthenticated)
        self.permission_classes = perms
        return super().get_permissions()

    @extend_schema(
        parameters=[
            OpenApiParameter("_class", type=int, description="Class ID"),
            OpenApiParameter("science", type=int, description="Science ID"),
            OpenApiParameter(
                "date", type=str, description="Date in format YYYY-MM-DD"
            ),
        ],
        summary="Get topic.",
        description="Get topic by date.",
        responses=serializers.TopicCalculationSerializer,
    )
    @decorators.action(
        methods=["GET"],
        detail=False,
        url_path="calculation",
        url_name="calculation",
    )
    def get_topic(self, request):
        ser = serializers.TopicFilterSerializer(data=request.GET)
        ser.is_valid(raise_exception=True)

        service = services.TopicService()
        date = ser.data.get("date", None)
        try:
            topic = service.get_topic_by_date(
                date if date else datetime.now().strftime("%d.%m.%Y"),
                ser.data.get("science"),
                ser.data.get("_class"),
                request.user,
            )
        except ValueError as e:
            raise exceptions.APIException(e)

        return Response(
            data=serializers.TopicCalculationSerializer(topic).data
        )
