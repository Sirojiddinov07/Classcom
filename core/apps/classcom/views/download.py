import datetime

from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.apps.classcom.models import (
    Download,
    DownloadToken,
    Media,
    Resource,
    Teacher,
)


class DownloadResourceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, resource_id, format=None):
        resource = get_object_or_404(Resource, id=resource_id)
        media = resource.media.first()
        if not media:
            raise Http404("Media not found for this resource")
        teacher = get_object_or_404(Teacher, user=request.user)
        download = Download.objects.create(
            teacher=teacher, resource=resource, date=datetime.date.today()
        )

        download_token = DownloadToken.objects.create(
            download=download,
            expires_at=timezone.now() + datetime.timedelta(minutes=5),
        )

        download_url = request.build_absolute_uri(
            reverse("download_file", args=[download_token.token])
        )

        return Response({"download_url": download_url})


class DownloadFileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, download_token, format=None):
        download_token = get_object_or_404(DownloadToken, token=download_token)

        if download_token.is_expired():
            raise Http404("Download link not found or expired")

        download = download_token.download

        if download.teacher.user != request.user:
            return Response(
                {"detail": "You are not authorized to download this file"},
                status=403,
            )

        media = get_object_or_404(Media, resource=download.resource)

        file_path = media.file.path
        response = FileResponse(open(file_path, "rb"))

        download_token.delete()

        return response

class DownloadHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        teacher = get_object_or_404(Teacher, user=request.user)
        downloads = Download.objects.filter(teacher=teacher).order_by('-date')

        download_history = [
            {
                "resource_id": download.resource.id,
                "resource_name": download.resource.name,  # Assuming Resource has a name field
                "download_date": download.date,
            }
            for download in downloads
        ]

        return Response({"download_history": download_history})
