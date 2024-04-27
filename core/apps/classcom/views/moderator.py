from rest_framework import viewsets
from core.apps.classcom import models
from core.apps.classcom import serializers


class ModeratorCreateViewSet(viewsets.ModelViewSet):
    queryset = models.Moderator.objects.all()
    serializer_class = serializers.ModeratorCreateSerializer

    def get_permissions(self):
        if self.action == 'create':
            return []
        return super().get_permissions()
