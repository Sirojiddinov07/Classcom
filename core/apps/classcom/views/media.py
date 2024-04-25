from rest_framework import viewsets, mixins
from core.apps.classcom import models, serializers


class MediaViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = serializers.MediaSerializer
    queryset = models.Media.objects.all()
