from django.db import models
from django.utils.translation import gettext_lazy as __

from core.http.models import User


class Moderator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.BigIntegerField(default=0)
    science = models.ForeignKey("Science", on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return str(self.user.first_name)

    class Meta:
        verbose_name = __("Moderator")
        verbose_name_plural = __("Moderators")
