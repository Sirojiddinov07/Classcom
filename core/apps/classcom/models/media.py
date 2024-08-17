from django.db import models
from django.utils.translation import gettext_lazy as __


class Media(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    desc = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to="media/")
    type = models.CharField(max_length=255, blank=True, null=True)
    file_type = models.CharField(max_length=255, blank=True, null=True)
    size = models.BigIntegerField(blank=True, null=True, default=0)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    download_users = models.ManyToManyField(
        "http.User", related_name="downloaded_media", blank=True
    )
    count = models.IntegerField(default=0)
    statistics = models.CharField(max_length=255, blank=True, null=True)

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
        verbose_name_plural = __("Medias")
