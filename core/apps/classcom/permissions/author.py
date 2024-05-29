from rest_framework import permissions


class IsAuthor(permissions.BasePermission):
    message = "You do not have permission to perform this operation."

    def __init__(self, model, pk):
        super().__init__()
        self.model = model
        self.pk = pk

    def __call__(self, *args, **kwargs):
        return self

    def has_permission(self, request, view):
        return self.model.objects.get(pk=self.pk).user == request.user
