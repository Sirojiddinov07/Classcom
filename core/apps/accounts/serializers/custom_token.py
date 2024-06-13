from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from core.http.serializers import UserSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        # Get user information
        user_serializer = UserSerializer(self.user)
        data['user'] = user_serializer.data

        return data
