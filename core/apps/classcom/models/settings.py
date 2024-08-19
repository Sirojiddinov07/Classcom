from django.db import models
from django.utils.translation import gettext_lazy as __

from core.http.models import AbstractBaseModel


class Settings(AbstractBaseModel):
    key = models.CharField(max_length=255, unique=True, verbose_name=__("Key"))
    value = models.TextField(verbose_name=__("Qiymati"))

    def __str__(self):
        return self.key

    class Meta:
        verbose_name = __("Sozlamalar")
        verbose_name_plural = __("Sozlamalar")
