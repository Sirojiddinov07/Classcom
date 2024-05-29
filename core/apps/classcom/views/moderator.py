from rest_framework import viewsets

from core.apps.classcom import models
from core.apps.classcom import serializers


class ModeratorViewSet(viewsets.ModelViewSet):
    queryset = models.Moderator.objects.all()
    serializer_class = serializers.ModeratorSerializer
