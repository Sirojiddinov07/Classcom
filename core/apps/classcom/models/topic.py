from django.db import models
from django.utils.translation import gettext_lazy as _

from core.http.models import AbstractBaseModel


class Topic(AbstractBaseModel):
    name = models.CharField(max_length=255, verbose_name=_("Nomi"))
    description = models.TextField(
        blank=True, null=True, verbose_name=_("Tavsif")
    )
    sequence_number = models.IntegerField(
        default=1, verbose_name=_("Tartib raqami")
    )
    hours = models.PositiveIntegerField(default=0, verbose_name=_("Soatlar"))
    banner = models.ImageField(
        upload_to="topic/banner/",
        blank=True,
        null=True,
        verbose_name=_("Banner"),
    )
    media = models.ManyToManyField(
        "Media", related_name="topic", verbose_name=_("Media")
    )

    def __str__(self):
        return f"{self.name}, {self.id}"

    class Meta:
        verbose_name = _("Mavzu")
        verbose_name_plural = _("Mavzular")
        ordering = ["sequence_number"]
