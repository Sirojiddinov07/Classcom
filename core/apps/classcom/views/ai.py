from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.apps.classcom.choices import Role
from core.apps.classcom.models import Ai
from core.apps.classcom.serializers import AiSerializer


class AiAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        topic = request.query_params.get("topic", None)
        queryset = Ai.objects.all()
        if topic is not None:
            queryset = queryset.filter(topic=topic)
        serializer = AiSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        if not request.user.role == Role.MODERATOR:
            raise PermissionDenied(
                _("Sizda buni amalga oshirishga ruxsat yo'q.")
            )

        if isinstance(request.data, list):
            for item in request.data:
                item_serializer = AiSerializer(
                    data=item, context={"request": request}
                )
                item_serializer.is_valid(raise_exception=True)
                item_serializer.save(user=request.user)
            return Response(status=status.HTTP_201_CREATED)
        else:
            serializer = AiSerializer(
                data=request.data, context={"request": request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def patch(self, request, *args, **kwargs):
        instance_id = request.query_params.get("id")
        if not instance_id:
            return Response(
                {"detail": _("ID is required.")},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            instance = Ai.objects.get(id=instance_id)
        except Ai.DoesNotExist:
            return Response(
                {"detail": _("Instance not found.")},
                status=status.HTTP_404_NOT_FOUND,
            )

        if instance.user != request.user:
            raise PermissionDenied(
                _("Sizda buni amalga oshirishga ruxsat yo'q.")
            )

        serializer = AiSerializer(
            instance,
            data=request.data,
            partial=True,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
