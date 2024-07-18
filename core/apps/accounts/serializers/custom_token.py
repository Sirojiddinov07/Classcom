from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from core.apps.classcom.models import Moderator
from core.http.serializers import UserSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        user_serializer = UserSerializer(self.user, context={
            "user": self.user
        })
        data["user"] = user_serializer.data

        # Check if the user is a moderator
        if self.user.role == "moderator":
            try:
                moderator = Moderator.objects.get(user=self.user)
                data["user"]["is_contracted"] = moderator.is_contracted
            except Moderator.DoesNotExist:
                data["user"]["is_contracted"] = False
        else:
            # If user is not a moderator, do not include is_contracted field
            data["user"].pop("is_contracted", None)

        return data
