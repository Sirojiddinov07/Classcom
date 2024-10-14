from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.apps.classcom.models import PlanAppeal
from core.apps.classcom.serializers.rtm_appeal import PlanAppealSerializer


class PlanAppealView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = PlanAppealSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            try:
                instance = serializer.save()
                return Response(
                    PlanAppealSerializer(instance).data,
                    status=status.HTTP_201_CREATED,
                )
            except Exception as e:
                return Response(
                    {"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        queryset = PlanAppeal.objects.filter(user=request.user)
        serializer = PlanAppealSerializer(queryset, many=True)
        return Response(serializer.data)
