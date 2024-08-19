from django.db import models
from django.utils.translation import gettext_lazy as __

from core.http.models import AbstractBaseModel


class Teacher(AbstractBaseModel):
    user = models.ForeignKey(
        "http.User", on_delete=models.CASCADE, verbose_name=__("Foydalanuvchi")
    )
    science = models.ManyToManyField(
        "Science", blank=True, verbose_name=__("Fanlar")
    )
    payment_status = models.BooleanField(
        default=False, verbose_name=__("To'lov holati")
    )

    def __str__(self):
        return self.user.first_name

    class Meta:
        verbose_name = __("O'qituvchi")
        verbose_name_plural = __("O'qituvchilar")
