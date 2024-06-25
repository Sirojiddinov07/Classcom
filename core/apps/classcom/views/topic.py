from rest_framework import viewsets, decorators, permissions, exceptions
from rest_framework.response import Response
from datetime import datetime
from core.apps.classcom import models, serializers, services


class TopicViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Topic.objects.all()
    serializer_class = serializers.TopicSerializer

    def get_permissions(self):
        perms = []
        match self.action:
            case "get_topic":
                perms.append(permissions.IsAuthenticated)
        self.permission_classes = perms
        return super().get_permissions()

    @decorators.action(
        methods=["GET"],
        detail=False,
        url_path="now",
        url_name="now",
    )
    def get_topic(self, request):
        ser = serializers.TopicFilterSerializer(data=request.GET)
        ser.is_valid(raise_exception=True)

        service = services.TopicService()
        try:
            topic = service.get_topic_by_date(
                datetime.now().strftime("%d.%m.%Y"),
                ser.data.get("science"),
                ser.data.get("_class"),
                request.user,
            )
        except ValueError as e:
            raise exceptions.APIException(e)

        return Response(data=serializers.TopicNowSerializer(topic).data)
