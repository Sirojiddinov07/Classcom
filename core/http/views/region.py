from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from core.apps.classcom.serializers import DistrictSerializer
from core.http.choices import Region, District


class GenerateDistrictsView(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request, region_id):
        try:
            region = Region.objects.get(id=region_id)
        except Region.DoesNotExist:
            return Response({"error": "Region not found"}, status=status.HTTP_404_NOT_FOUND)

        districts = District.objects.filter(region=region)
        serializer = DistrictSerializer(districts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)