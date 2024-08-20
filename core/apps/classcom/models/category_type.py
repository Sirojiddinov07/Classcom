from django.db import models
from django.utils.translation import gettext_lazy as _

from core.http.models import AbstractBaseModel


class CategoryType(AbstractBaseModel):
    name = models.CharField(max_length=255, verbose_name=_("Kategoriya turi"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Kategoriya turi")
        verbose_name_plural = _("Kategoriyalar turi")
