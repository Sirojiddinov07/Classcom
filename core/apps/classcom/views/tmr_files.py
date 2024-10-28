from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from core.apps.classcom.models import TmrFiles
from core.apps.classcom.serializers.tmr_files import TmrFilesSerializer
from core.apps.classcom.views.tmr_appeal import IsModerator


class TmrFilesAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsModerator]

    def get(self, request, *args, **kwargs):
        tmr_id = request.query_params.get("tmr_id")
        if not tmr_id:
            return Response(
                {"tmr_id": ["This field is required."]},
                status=status.HTTP_400_BAD_REQUEST,
            )
        files = TmrFiles.objects.filter(tmr_appeal=tmr_id)
        serializer = TmrFilesSerializer(
            files, many=True, context={"request": request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = TmrFilesSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
