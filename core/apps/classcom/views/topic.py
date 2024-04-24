from rest_framework import viewsets, permissions

from core.apps.classcom import models, serializers


class TopicViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Topic.objects.all()
    serializer_class = serializers.TopicSerializer
