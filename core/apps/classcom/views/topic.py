from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions

from core.apps.classcom import models, serializers


class TopicViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Topic.objects.all()
    serializer_class = serializers.TopicSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['_class', 'quarter', 'science']