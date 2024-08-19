from django.db import models
from django.utils.translation import gettext_lazy as __

from core.http.models import AbstractBaseModel


class Media(AbstractBaseModel):
    name = models.CharField(
        max_length=255, blank=True, null=True, verbose_name=__("Nomi")
    )
    desc = models.TextField(blank=True, null=True, verbose_name=__("Tavsif"))
    file = models.FileField(upload_to="media/", verbose_name=__("Fayl"))
    type = models.CharField(
        max_length=255, blank=True, null=True, verbose_name=__("Turi")
    )
    file_type = models.CharField(
        max_length=255, blank=True, null=True, verbose_name=__("Fayl turi")
    )
    size = models.BigIntegerField(
        blank=True, null=True, default=0, verbose_name=__("Hajmi")
    )

    download_users = models.ManyToManyField(
        "http.User",
        related_name="downloaded_media",
        blank=True,
        verbose_name=__("Yuklab olganlar"),
    )
    count = models.IntegerField(default=0, verbose_name=__("Yuklashlar soni"))
    statistics = models.CharField(
        max_length=255, blank=True, null=True, verbose_name=__("Statistika")
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
        verbose_name = __("Media")
        verbose_name_plural = __("Medialar")
