from django.db import models
from django.utils.translation import gettext_lazy as _

from core.http.models import AbstractBaseModel


class Document(AbstractBaseModel):
    title = models.CharField(_("Nomi"), max_length=255, blank=True, null=True)
    description = models.TextField(_("Tasnifi"), blank=True, null=True)
    file = models.FileField(_("Fayl"), upload_to="documents/%Y/%m/%d/")
    is_active = models.BooleanField(_("Holati"), default=True)
    type = models.CharField(_("Turi"), max_length=255, blank=True, null=True)
    size = models.BigIntegerField(_("Hajmi"), blank=True, null=True, default=0)

    class Meta:
        verbose_name = _("Hujjat")
        verbose_name_plural = _("Hujjatlar")

    def __str__(self):
        return f"{self.title} - {self.file.name} - {self.type}"

    def save(self, *args, **kwargs):
        self.type = self.file.name.split(".")[-1]
        self.size = self.file.size
        if self.title is None:
            self.title = (
                self.file.name
                if self.file.name is not None
                else f"Media {self.id}"
            )
            self.description = f"{self.title}"
        super().save(*args, **kwargs)

    @property
    def url(self):
        return self.file.url
