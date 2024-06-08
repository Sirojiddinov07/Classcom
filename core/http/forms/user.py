from django.contrib.auth.forms import UserCreationForm
from core.http.models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("phone",)
