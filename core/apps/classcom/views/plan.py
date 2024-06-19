from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination

from core.apps.classcom import models
from core.apps.classcom import serializers

class PlanPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'



class PlanViewSet(viewsets.ModelViewSet):
    queryset = models.Plan.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["classes", "topic", "hour", "quarter"]
    pagination_class = PlanPagination

    def get_serializer_class(self):
        if self.request.method == "GET":
            if self.action == "retrieve":
                return serializers.PlanDetailSerializer
            return serializers.PlanSerializer
        return serializers.PlanCreateSerializer
