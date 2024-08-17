import datetime

from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.apps.classcom.models import (
    Download,
    DownloadToken,
    Media,
    Teacher,
    Plan,
    Moderator,
)
from core.apps.payments.models import Orders


class DownloadMediaView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, media_id, format=None):
        media = get_object_or_404(Media, id=media_id)
        if not media:
            raise Http404("Media not found for this resource")
        teacher = get_object_or_404(Teacher, user=request.user)
        plan = Plan.objects.filter(plan_resource=media).first()
        if not plan:
            raise Http404("Plan not found for this media")
        moderator = get_object_or_404(Moderator, user=plan.user)
        download = Download.objects.create(
            teacher=teacher,
            media=media,
            date=datetime.date.today(),
            moderator=moderator,
        )

        if download.media.download_users.filter(id=request.user.id).exists():
            pass
        download.media.download_users.add(request.user)
        download.media.count += 1
        download.media.save()

        science = Plan.objects.filter(plan_resource=media).first().science
        users_count = (
            Orders.objects.filter(science=science)
            .values("user")
            .distinct()
            .count()
        )
        download_users_count = download.media.download_users.count()

        download.media.statistics = (
            f"{(users_count / download_users_count) * 100}%"
        )
        download.media.save()

        download_token = DownloadToken.objects.create(
            download=download,
            expires_at=timezone.now() + datetime.timedelta(minutes=5),
        )

        download_url = download_token.token

        return Response({"download_token": download_url})


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

        media = get_object_or_404(Media, resources=download.media)

        file_path = media.file.path
        response = FileResponse(open(file_path, "rb"))

        download_token.delete()

        return response


class DownloadHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        teacher = get_object_or_404(Teacher, user=request.user)
        downloads = (
            Download.objects.filter(teacher=teacher)
            .order_by("-date")
            .distinct()
        )

        download_history = [
            {
                "media_id": download.media.id,
                "media_name": download.media.name,
                "download_date": download.date,
            }
            for download in downloads
        ]

        return Response({"download_history": download_history})
