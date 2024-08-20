from django.db import models
from django.utils.translation import gettext_lazy as _

from core.http.models import AbstractBaseModel


class Download(AbstractBaseModel):
    teacher = models.ForeignKey(
        "Teacher",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name=_("O'qituvchi"),
    )
    moderator = models.ForeignKey(
        "Moderator",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name=_("Moderator"),
    )
    date = models.DateField(verbose_name=_("Sanasi"))
    media = models.ForeignKey(
        "Media", on_delete=models.CASCADE, verbose_name=_("Media")
    )

    def __str__(self):
        return super().__str__()

    class Meta:
        verbose_name = _("Yuklamalar")
        verbose_name_plural = _("Yuklamalar")
