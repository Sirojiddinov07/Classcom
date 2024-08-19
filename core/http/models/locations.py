from django.db import models
from django.utils.translation import gettext_lazy as _

from core.http.models import AbstractBaseModel


class Region(AbstractBaseModel):
    region = models.CharField(max_length=255, verbose_name=_("Viloyat"))

    def __str__(self):
        return self.region

    class Meta:
        verbose_name = _("Viloyat")
        verbose_name_plural = _("Viloyatlar")


class District(AbstractBaseModel):
    district = models.CharField(max_length=255, verbose_name=_("Tuman"))
    region = models.ForeignKey(
        "Region",
        on_delete=models.CASCADE,
        related_name="districts",
        verbose_name=_("Viloyat"),
    )

    def __str__(self):
        return self.district

    class Meta:
        verbose_name = _("Tuman")
        verbose_name_plural = _("Tumanlar")
