from rest_framework import viewsets
from . import models
from . import serializers


class ModeratorViewSet(viewsets.ModelViewSet):
    queryset = models.Moderator.objects.all()
    serializer_class = serializers.ModeratorSerializer
