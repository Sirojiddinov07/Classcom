from django.db.models import Count
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from core.apps.classcom.models.moderator import Moderator


class ModeratorCountsByScienceAndClassAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, science_id):
        results = (
            Moderator.objects.filter(science_id=science_id)
            .values(
                "science__id", "science__name", "classes__id", "classes__name"
            )
            .annotate(moderator_count=Count("id"))
            .order_by("classes")
        )

        formatted_results = [
            {
                "science_id": result["science__id"],
                "science_name": result["science__name"],
                "class_id": result["classes__id"],
                "class_name": result["classes__name"],
                "moderator_count": result["moderator_count"],
            }
            for result in results
        ]

        return Response(formatted_results)
