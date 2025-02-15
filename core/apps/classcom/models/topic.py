from django.db import models
from django.utils.translation import gettext_lazy as _

from core.http.models import AbstractBaseModel


class Topic(AbstractBaseModel):
    plan_id = models.ForeignKey(
        "Plan", on_delete=models.CASCADE, related_name="topic"
    )
    name = models.CharField(max_length=255, verbose_name=_("Nomi"))
    description = models.TextField(
        blank=True, null=True, verbose_name=_("Tavsif")
    )
    sequence_number = models.IntegerField(
        default=1, verbose_name=_("Tartib raqami")
    )
    hours = models.PositiveIntegerField(default=0, verbose_name=_("Soatlar"))
    media = models.ManyToManyField(
        "Media", related_name="topic", verbose_name=_("Media"), blank=True
    )
    media_creatable = models.BooleanField(
        default=False, verbose_name=_("Resurs yarata olishi.")
    )
    weeks = models.PositiveIntegerField(
        default=1, verbose_name=_("Haftalar"), blank=True, null=True
    )
    user = models.ForeignKey(
        "http.User",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="topic",
        verbose_name=_("Foydalanuvchi"),
    )
    banner = models.ImageField(
        upload_to="topic/banner/",
        verbose_name=_("Banner"),
        blank=True,
        null=True,
    )
    view_count = models.PositiveBigIntegerField(
        default=0, verbose_name=_("Ko'rishlar soni")
    )

    def __str__(self):
        return f"{self.name}, {self.sequence_number}"

    class Meta:
        verbose_name = _("Mavzu")
        verbose_name_plural = _("Mavzular")
        ordering = ["sequence_number"]

    @property
    def media_count(self):
        return self.media.count()

    @property
    def all_download_count(self):
        return sum(
            [media.download_users.count() for media in self.media.all()]
        )
