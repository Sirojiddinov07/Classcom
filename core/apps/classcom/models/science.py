from django.db import models
from django.utils.translation import gettext_lazy as _

from core.http.models import ScienceGroups, AbstractBaseModel


class ScienceTypes(AbstractBaseModel):
    name = models.CharField(verbose_name=_("Nomi"))

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = _("Fan turi")
        verbose_name_plural = _("Fan turlari")


class Science(AbstractBaseModel):
    name = models.CharField(verbose_name=_("Nomi"))
    science_grp = models.ForeignKey(
        ScienceGroups,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=_("Fan guruhi"),
    )
    types = models.ManyToManyField(ScienceTypes, verbose_name=_("Fan turi"))
    order_number = models.PositiveIntegerField(
        verbose_name=_("Tartib raqami"), blank=True, null=True
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.pk:  # Yangi qator qo'shilayotgan bo'lsa
            if self.order_number is None:
                max_order_number = (
                    Science.objects.aggregate(models.Max("order_number"))[
                        "order_number__max"
                    ]
                    or 0
                )
                self.order_number = max_order_number + 1
            else:
                # Order_number ga yangi tartib raqami kiritilgan bo'lsa
                Science.objects.filter(
                    order_number__gte=self.order_number
                ).update(order_number=models.F("order_number") + 1)
        else:
            # Yangi tartibga o'zgartirish (eski va yangi order_numberni solishtirib, qatorlarni surish)
            old_instance = Science.objects.get(pk=self.pk)
            if (
                self.order_number is not None
                and old_instance.order_number is not None
            ):
                if self.order_number < old_instance.order_number:
                    Science.objects.filter(
                        order_number__gte=self.order_number,
                        order_number__lt=old_instance.order_number,
                    ).update(order_number=models.F("order_number") + 1)
                else:
                    Science.objects.filter(
                        order_number__gt=old_instance.order_number,
                        order_number__lte=self.order_number,
                    ).update(order_number=models.F("order_number") - 1)

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("Fan")
        verbose_name_plural = _("Fanlar")
