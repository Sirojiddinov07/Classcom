from django.db import models
from django.utils.translation import gettext_lazy as _

from core.http.models import AbstractBaseModel


class Settings(AbstractBaseModel):
    key = models.CharField(max_length=255, unique=True, verbose_name=_("Key"))
    value = models.TextField(verbose_name=_("Qiymati"))

    def __str__(self):
        return self.key

    class Meta:
        verbose_name = _("Sozlamalar")
        verbose_name_plural = _("Sozlamalar")
