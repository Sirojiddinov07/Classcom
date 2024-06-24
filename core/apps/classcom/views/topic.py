from rest_framework import viewsets, decorators, permissions
from rest_framework.response import Response

from core.apps.classcom import models, serializers


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
        url_path="get-topic/<_class:int>/<science:int>/",
        url_name="get-topic",
    )
    def get_topic(self, request, _class, science):
        return Response(science, _class)
