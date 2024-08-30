from django.db import models
from django.utils.translation import gettext_lazy as _

from core.apps.classcom.choices import Types
from core.apps.classcom.utils.dynamic_sort import OrderNumberService
from core.http.models import AbstractBaseModel


class ResourceType(AbstractBaseModel):
    name = models.CharField(max_length=255, verbose_name=_("Nomi"))
    type = models.CharField(
        choices=Types.choices, verbose_name=_("Turi"), max_length=255
    )
    order_number = models.PositiveIntegerField(
        verbose_name=_("Tartib raqami"), blank=True, null=True
    )
    is_active = models.BooleanField(default=True, verbose_name=_("Aktiv"))

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        OrderNumberService.update_order_numbers(self, "order_number")
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("Resurs turi")
        verbose_name_plural = _("Resurs turlari")
        ordering = ["order_number"]
