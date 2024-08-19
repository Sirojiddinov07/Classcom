from django.db import models
from django.utils.translation import gettext_lazy as __

from core.http.models import AbstractBaseModel


class CategoryType(AbstractBaseModel):
    name = models.CharField(max_length=255, verbose_name=__("Kategoriya turi"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = __("Kategoriya turi")
        verbose_name_plural = __("Kategoriyalar turi")
