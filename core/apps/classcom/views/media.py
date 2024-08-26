from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from core.apps.classcom.models import Topic, Media
from core.apps.classcom.serializers.media import (
    MediaDetailSerializer,
    MediaSerializer,
)


class MediaApiView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        media_id = request.query_params.get("id")
        topic_id = request.query_params.get("topic_id")

        if media_id:
            try:
                media = Media.objects.get(id=media_id)
                serializer = MediaDetailSerializer(media)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Media.DoesNotExist:
                return Response(
                    {"error": "Media not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )

        if topic_id:
            try:
                topic = Topic.objects.get(id=topic_id)
                media = topic.media.all()
                serializer = MediaDetailSerializer(media, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Topic.DoesNotExist:
                return Response(
                    {"error": "Topic not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )

        return Response(
            {"error": "media_id is required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def post(self, request):
        topic_id = request.query_params.get("topic_id")
        if not topic_id:
            return Response(
                {"error": "topic_id is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            topic = Topic.objects.get(id=topic_id)
        except Topic.DoesNotExist:
            return Response(
                {"error": "Topic not found"}, status=status.HTTP_404_NOT_FOUND
            )

        if not isinstance(request.data, list):
            return Response(
                {"error": "Request data must be a list of dictionaries"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        media_data = []
        for media_item in request.data:
            if not isinstance(media_item, dict):
                return Response(
                    {"error": "Each media item must be a dictionary"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            media_file = request.FILES.get(media_item.get("file"))
            if not media_file:
                return Response(
                    {"error": "File is required for each media item"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            media_data.append(
                {"file": media_file, "desc": media_item.get("desc")}
            )

        serializer = MediaSerializer(data=media_data, many=True)
        if serializer.is_valid():
            serializer.save()
            topic.media.add(*serializer.instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        media_id = request.query_params.get("id")
        if not media_id:
            return Response(
                {"error": "media_id is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            media = Media.objects.get(id=media_id)
        except Media.DoesNotExist:
            return Response(
                {"error": "Media not found"}, status=status.HTTP_404_NOT_FOUND
            )

        media.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request):
        media_id = request.query_params.get("id")
        if not media_id:
            return Response(
                {"error": "media_id is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            media = Media.objects.get(id=media_id)
        except Media.DoesNotExist:
            return Response(
                {"error": "Media not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = MediaSerializer(media, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
