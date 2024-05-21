from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend


from core.apps.classcom import models
from core.apps.classcom import serializers


class PlanViewSet(viewsets.ModelViewSet):
    queryset = models.Plan.objects.all()
    serializer_class = serializers.PlanSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['classes', 'topic', 'hour']
