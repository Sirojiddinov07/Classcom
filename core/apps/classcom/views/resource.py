from rest_framework import viewsets
from core.apps.classcom import models, serializers, permissions, choices
from core.http import permissions as http_permissions


class ResourceViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return models.Resource.objects.filter(user=self.request.user).order_by("-id")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_permissions(self):
        if self.action == "retrieve":
            return [
                permissions.IsAuthor(models.Resource, self.kwargs.get("pk")),
                http_permissions.HasRole([
                    choices.Role.MODERATOR,
                    choices.Role.ADMIN
                ])
            ]
        return []

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.ResourceDetailSerializer
        return serializers.ResourceSerializer
