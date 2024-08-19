from rest_framework import serializers
from django.utils.translation import gettext_lazy as _


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate(self):
        if self.context.get("request").user is None:
            raise serializers.ValidationError(
                {
                    "detail": _(
                        "Foydalanuvchi topilmadi. Iltimos, qayta kirishni urinib ko'ring."
                    ),
                }
            )
