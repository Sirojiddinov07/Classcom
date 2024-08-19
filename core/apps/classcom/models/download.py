from django.db import models
from django.utils.translation import gettext_lazy as __

from core.http.models import AbstractBaseModel


class Download(AbstractBaseModel):
    teacher = models.ForeignKey(
        "Teacher",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name=__("O'qituvchi"),
    )
    moderator = models.ForeignKey(
        "Moderator",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name=__("Moderator"),
    )
    date = models.DateField(verbose_name=__("Sanasi"))
    media = models.ForeignKey(
        "Media", on_delete=models.CASCADE, verbose_name=__("Media")
    )

    def __str__(self):
        return super().__str__()

    class Meta:
        verbose_name = __("Yuklamalar")
        verbose_name_plural = __("Yuklamalar")
