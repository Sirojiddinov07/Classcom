from django.db import models
from django.utils.translation import gettext_lazy as _

from core.apps.classcom.choices import Types
from core.http.models import AbstractBaseModel


class ResourceType(AbstractBaseModel):
    name = models.CharField(max_length=255, verbose_name=_("Nomi"))
    type = models.CharField(
        choices=Types.choices, verbose_name=_("Turi"), max_length=255
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Resurs turi")
        verbose_name_plural = _("Resurs turlari")
