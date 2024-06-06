from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

from core.apps.classcom import models
from core.apps.classcom import serializers


class PlanViewSet(viewsets.ModelViewSet):
    queryset = models.Plan.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['classes', 'topic', 'hour']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.PlanDetailSerializer
        return serializers.PlanCreateSerializer
