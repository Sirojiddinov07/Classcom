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
    media = models.ManyToManyField(
        "Media", related_name="topic", verbose_name=_("Media")
    )
    media_creatable = models.BooleanField(
        default=False, verbose_name=_("Media yarata olishi.")
    )

    # media_creatable = models.BooleanField(
    #     default=False, verbose_name=_("Media yarata olishi.")
    # )
    # media_creatable_users = models.ManyToManyField(
    #     "http.User",
    #     blank=True,
    #     related_name="media_creatable",
    #     verbose_name=_("Media yarata olishi."),
    # )

    def __str__(self):
        return f"{self.name}, {self.id}"

    class Meta:
        verbose_name = _("Mavzu")
        verbose_name_plural = _("Mavzular")
        ordering = ["sequence_number"]
