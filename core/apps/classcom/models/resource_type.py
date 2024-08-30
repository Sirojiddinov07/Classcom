from django.db import models
from django.utils.translation import gettext_lazy as _

from core.apps.classcom.choices import Types
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
        if not self.pk:  # Yangi qator qo'shilayotgan bo'lsa
            if self.order_number is None:
                max_order_number = (
                    ResourceType.objects.aggregate(models.Max("order_number"))[
                        "order_number__max"
                    ]
                    or 0
                )
                self.order_number = max_order_number + 1
            else:
                # Order_number ga yangi tartib raqami kiritilgan bo'lsa
                ResourceType.objects.filter(
                    order_number__gte=self.order_number
                ).update(order_number=models.F("order_number") + 1)
        else:
            # Yangi tartibga o'zgartirish (eski va yangi order_numberni solishtirib, qatorlarni surish)
            old_instance = ResourceType.objects.get(pk=self.pk)
            if (
                self.order_number is not None
                and old_instance.order_number is not None
            ):
                if self.order_number < old_instance.order_number:
                    ResourceType.objects.filter(
                        order_number__gte=self.order_number,
                        order_number__lt=old_instance.order_number,
                    ).update(order_number=models.F("order_number") + 1)
                else:
                    ResourceType.objects.filter(
                        order_number__gt=old_instance.order_number,
                        order_number__lte=self.order_number,
                    ).update(order_number=models.F("order_number") - 1)

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("Resurs turi")
        verbose_name_plural = _("Resurs turlari")
        ordering = ["order_number"]
