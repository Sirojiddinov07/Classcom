from django.db import models
from django.utils.translation import gettext_lazy as _

from core.http.models import AbstractBaseModel


class Teacher(AbstractBaseModel):
    user = models.ForeignKey(
        "http.User", on_delete=models.CASCADE, verbose_name=_("Foydalanuvchi")
    )
    science = models.ManyToManyField(
        "Science", blank=True, verbose_name=_("Fanlar")
    )
    payment_status = models.BooleanField(
        default=False, verbose_name=_("To'lov holati")
    )

    def __str__(self):
        return self.user.first_name

    class Meta:
        verbose_name = _("O'qituvchi")
        verbose_name_plural = _("O'qituvchilar")
