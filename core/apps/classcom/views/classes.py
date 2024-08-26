from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from core.apps.classcom import models, serializers
from core.apps.classcom.views.region import CustomPagination


class ClassesViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows classes to be viewed or edited.
    """

    permission_classes = [AllowAny]
    queryset = models.Classes.objects.all()
    serializer_class = serializers.ClassesSerializer
    pagination_class = CustomPagination


class ClassTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows class types to be viewed or edited.
    """

    permission_classes = [AllowAny]
    queryset = models.ClassType.objects.all()
    serializer_class = serializers.ClassTypeSerializer
    pagination_class = CustomPagination
