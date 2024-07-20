from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from core.apps.classcom import models, serializers


class ClassesViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows classes to be viewed or edited.
    """

    permission_classes = [AllowAny]
    queryset = models.Classes.objects.all()
    serializer_class = serializers.ClassesSerializer
