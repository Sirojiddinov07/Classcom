import datetime

from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.apps.classcom.choices import Role
from core.apps.classcom.models import (
    Download,
    DownloadToken,
    Teacher,
)
from core.apps.classcom.models import Media, Plan, Moderator
from core.apps.classcom.views import CustomPagination
from core.apps.payments.models import Orders


class DownloadMediaView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, media_id, format=None):
        user = request.user
        current_date = datetime.date.today()
        media = get_object_or_404(Media, id=media_id)
        teacher = (
            get_object_or_404(Teacher, user=user)
            if Teacher.objects.filter(user=user).exists()
            else None
        )

        # Check if media has an associated topic
        plan = Plan.objects.filter(topic__media=media).first()
        moderator = (
            get_object_or_404(Moderator, user=plan.user) if plan else None
        )

        order = Orders.objects.filter(
            user=user,
            science=plan.science,
            types=plan.science_types,
            start_date__lt=current_date,
            end_date__gt=current_date,
        ).first()

        # If media has a topic, only the owner or a user with an order can download
        if plan and (
            media.user != user and (not order and user.role != Role.MODERATOR)
        ):
            raise Http404("You can't download this file")

        download = Download.objects.create(
            teacher=teacher,
            media=media,
            date=current_date,
            moderator=moderator,
        )

        if plan:
            if user.role != Role.MODERATOR:
                if not download.media.download_users.filter(
                    id=user.id
                ).exists():
                    download.media.download_users.add(user)
                    download.media.count += 1
                    download.media.save()
        else:
            if not download.media.download_users.filter(id=user.id).exists():
                download.media.download_users.add(user)
                download.media.count += 1
                download.media.save()

        science = plan.science if plan else None
        users_count = (
            (
                Orders.objects.filter(science=science)
                .values("user")
                .distinct()
                .count()
            )
            if science
            else 0
        )

        users_count = min(users_count, 1)
        download_users_count = download.media.download_users.count()

        download.media.statistics = (
            (f"{(users_count / download_users_count) * 100}%")
            if download_users_count > 0
            else "0%"
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
            raise Http404("Download token not found or expired")

        download = download_token.download

        media = get_object_or_404(Media, id=download.media.id)

        file_path = media.file.path

        try:
            response = FileResponse(open(file_path, "rb"))
        except FileNotFoundError:
            raise Http404("File not found")

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


############################################################################################################
# Moderator yuklagan resurs media fayllarini ro'yxatini olish
############################################################################################################
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def moderator_media_list(request):
    if not Moderator.objects.filter(user=request.user).exists():
        return Response({"detail": "User is not a moderator"}, status=403)

    moderator = Moderator.objects.get(user=request.user)

    media_files = Media.objects.filter(user=moderator.user).distinct()

    paginator = CustomPagination()
    paginated_media = paginator.paginate_queryset(media_files, request)

    media_list = [
        {
            "id": media.id,
            "name": media.name,
            "file_type": media.type,
            "desc": media.desc,
            "size": media.size,
            "count": media.count,
            "statistics": media.statistics,
            "created_at": media.created_at,
            "updated_at": media.updated_at,
        }
        for media in paginated_media
    ]

    total_media_count = media_files.count()

    response_data = {
        "total_media_count": total_media_count,
        "media_files": media_list,
    }

    return paginator.get_paginated_response(response_data)
