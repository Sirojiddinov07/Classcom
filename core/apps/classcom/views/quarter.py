# classcom/views.py
from rest_framework import generics

from core.apps.classcom.models import Quarter
from core.apps.classcom.serializers import QuarterMiniSerializer


class QuarterListView(generics.ListAPIView):
    queryset = Quarter.objects.all().order_by('choices')
    serializer_class = QuarterMiniSerializer
