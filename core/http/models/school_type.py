from django.db import models
from django.utils.translation import gettext_lazy as _

from core.http.choices import Institution
from core.http.models import AbstractBaseModel


class SchoolType(AbstractBaseModel):
    name = models.CharField(max_length=255, verbose_name=_("Maktab turi"))
    institution = models.CharField(
        max_length=255,
        choices=Institution.choices,
        null=True,
        blank=True,
        verbose_name=_("Muassasa"),
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Maktab turi")
        verbose_name_plural = _("Maktab turlari")
