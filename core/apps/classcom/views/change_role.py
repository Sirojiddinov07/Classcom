# views.py
from rest_framework import status, views
from rest_framework.response import Response

from core.apps.classcom.choices import Role
from core.http.models import User
from core.http.serializers import UserRoleChangeSerializer


class UserRoleChangeView(views.APIView):
    def post(self, request, *args, **kwargs):
        user = User.objects.get(pk=kwargs["pk"])
        if user.role != Role.USER:
            return Response(
                {
                    "detail": "Only users with "
                    "the USER role can change their role."
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = UserRoleChangeSerializer(
            user, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
