from django.db.models import Count, Q
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from core.apps.classcom.models.classes import Classes
from core.apps.classcom.models.moderator import (
    Moderator,
)


class ModeratorCountsByScienceAndClassAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, science_id):
        all_classes = Classes.objects.annotate(
            moderator_count=Count(
                "moderator", filter=Q(moderator__science_id=science_id)
            )
        ).order_by("-moderator_count")

        science_name = (
            Moderator.objects.filter(science_id=science_id)
            .first()
            .science.name
            if Moderator.objects.filter(science_id=science_id).exists()
            else None
        )

        formatted_results = [
            {
                "class_id": cls.id,
                "class_name": cls.name,
                "science_id": science_id,
                "science_name": science_name,
                "moderator_count": cls.moderator_count,
            }
            for cls in all_classes
        ]

        return Response(formatted_results)
