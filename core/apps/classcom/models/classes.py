from django.db import models
from django.utils.translation import gettext_lazy as _

from core.http.models import AbstractBaseModel


class ClassType(AbstractBaseModel):
    name = models.CharField(max_length=255, verbose_name=_("Sinf guruhi nomi"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Sinf Guruhi")
        verbose_name_plural = _("Sinf Guruhlari")


class Classes(AbstractBaseModel):
    name = models.CharField(max_length=255, verbose_name=_("Sinf nomi"))
    type = models.ForeignKey(
        ClassType,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=_("Sinf guruhi"),
    )
    order_number = models.PositiveIntegerField(
        null=True, blank=True, verbose_name=_("Tartib raqami")
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.pk:  # Yangi qator qo'shilayotgan bo'lsa
            if self.order_number is None:
                max_order_number = (
                    Classes.objects.aggregate(models.Max("order_number"))[
                        "order_number__max"
                    ]
                    or 0
                )
                self.order_number = max_order_number + 1
            else:
                # Order_number ga yangi tartib raqami kiritilgan bo'lsa
                Classes.objects.filter(
                    order_number__gte=self.order_number
                ).update(order_number=models.F("order_number") + 1)
        else:
            # Yangi tartibga o'zgartirish (eski va yangi order_numberni solishtirib, qatorlarni surish)
            old_instance = Classes.objects.get(pk=self.pk)
            if (
                self.order_number is not None
                and old_instance.order_number is not None
            ):
                if self.order_number < old_instance.order_number:
                    Classes.objects.filter(
                        order_number__gte=self.order_number,
                        order_number__lt=old_instance.order_number,
                    ).update(order_number=models.F("order_number") + 1)
                else:
                    Classes.objects.filter(
                        order_number__gt=old_instance.order_number,
                        order_number__lte=self.order_number,
                    ).update(order_number=models.F("order_number") - 1)

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("Sinf")
        verbose_name_plural = _("Sinflar")
        ordering = ("order_number",)
