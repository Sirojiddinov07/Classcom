from rest_framework import permissions, viewsets

from core.apps.classcom import models, serializers


class ClassesViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows classes to be viewed or edited.
    """

    queryset = models.Classes.objects.all()
    serializer_class = serializers.ClassesSerializer
