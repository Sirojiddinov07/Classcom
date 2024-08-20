from django.db import models
from django.utils.translation import gettext_lazy as _

from core.http.models import AbstractBaseModel


class Media(AbstractBaseModel):
    name = models.CharField(
        max_length=255, blank=True, null=True, verbose_name=_("Nomi")
    )
    desc = models.TextField(blank=True, null=True, verbose_name=_("Tavsif"))
    file = models.FileField(upload_to="media/", verbose_name=_("Fayl"))
    type = models.CharField(
        max_length=255, blank=True, null=True, verbose_name=_("Turi")
    )
    file_type = models.CharField(
        max_length=255, blank=True, null=True, verbose_name=_("Fayl turi")
    )
    size = models.BigIntegerField(
        blank=True, null=True, default=0, verbose_name=_("Hajmi")
    )

    download_users = models.ManyToManyField(
        "http.User",
        related_name="downloaded_media",
        blank=True,
        verbose_name=_("Yuklab olganlar"),
    )
    count = models.IntegerField(default=0, verbose_name=_("Yuklashlar soni"))
    statistics = models.CharField(
        max_length=255, blank=True, null=True, verbose_name=_("Statistika")
    )

    def __str__(self) -> str:
        return str(self.name) if self.name is not None else f"Media {self.id}"

    def save(self, *args, **kwargs):
        self.file_type = self.file.name.split(".")[-1]
        self.size = self.file.size
        if self.name is None:
            self.name = (
                self.file.name
                if self.file.name is not None
                else f"Media {self.id}"
            )
        if self.name_uz is None:
            self.name_uz = (
                self.file.name
                if self.file.name is not None
                else f"Media {self.id}"
            )
        if self.name_ru is None:
            self.name_ru = (
                self.file.name
                if self.file.name is not None
                else f"Media {self.id}"
            )
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("Media")
        verbose_name_plural = _("Medialar")
