from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from core.apps.classcom.models import TmrFiles, TMRAppeal, TMRAppealStatus
from core.apps.classcom.serializers.tmr_files import TmrFilesSerializer
from core.apps.classcom.views.tmr_appeal import IsModerator


class TmrFilesAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsModerator]

    def get(self, request, *args, **kwargs):
        files = TmrFiles.objects.filter(tmr_appeal__user=request.user)
        serializer = TmrFilesSerializer(
            files, many=True, context={"request": request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        tmr_id = request.data.get("tmr_appeal")
        if not tmr_id:
            return Response(
                {"tmr_id": ["This field is required."]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            tmr_appeal = TMRAppeal.objects.get(id=tmr_id)
        except TmrFiles.DoesNotExist:
            return Response(
                {"tmr_id": ["Tmr appeal not found."]},
                status=status.HTTP_404_NOT_FOUND,
            )

        if tmr_appeal.status != TMRAppealStatus.ACCEPTED:
            return Response(
                {"detail": "Tmr appeal status must be accepted to post."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = TmrFilesSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
