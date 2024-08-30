from django.db import models
from django.utils.translation import gettext_lazy as _

from core.http.models import AbstractBaseModel
from ..choices import ResourceDegree


class Resource(AbstractBaseModel):
    category = models.ForeignKey(
        "Category",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=_("Kategoriya"),
    )
    category_type = models.ForeignKey(
        "CategoryType",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=_("Kategoriya turi"),
    )
    name = models.CharField(max_length=255, verbose_name=_("Nomi"))
    description = models.TextField(verbose_name=_("Tavsif"))

    banner = models.ImageField(
        upload_to="resource_banners/", verbose_name=_("Banner")
    )
    type = models.ForeignKey(
        "ResourceType",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=_("Resurs turi"),
    )
    subtype = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Resurs sub turi"),
    )

    user = models.ForeignKey(
        "http.User", on_delete=models.CASCADE, verbose_name=_("Foydalanuvchi")
    )
    classes = models.ForeignKey(
        "Classes",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=_("Sinflar"),
    )
    media = models.ManyToManyField(
        "Media", blank=True, related_name="resources", verbose_name=_("Media")
    )
    source = models.CharField(
        max_length=255, null=True, blank=True, verbose_name=_("Manba")
    )
    degree = models.CharField(
        choices=ResourceDegree.choices,
        default=ResourceDegree.MEDIUM,
        verbose_name=_("Daraja"),
    )
    order_number = models.PositiveIntegerField(
        verbose_name=_("Tartib raqami"), blank=True, null=True
    )
    science = models.ForeignKey(
        "Science",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=_("Fan"),
    )

    def __str__(self):
        return str(self.name) or "Unnamed Resource"

    def save(self, *args, **kwargs):
        if not self.pk:  # Yangi qator qo'shilayotgan bo'lsa
            if self.order_number is None:
                max_order_number = (
                    Resource.objects.aggregate(models.Max("order_number"))[
                        "order_number__max"
                    ]
                    or 0
                )
                self.order_number = max_order_number + 1
            else:
                # Order_number ga yangi tartib raqami kiritilgan bo'lsa
                Resource.objects.filter(
                    order_number__gte=self.order_number
                ).update(order_number=models.F("order_number") + 1)
        else:
            # Yangi tartibga o'zgartirish (eski va yangi order_numberni solishtirib, qatorlarni surish)
            old_instance = Resource.objects.get(pk=self.pk)
            if (
                self.order_number is not None
                and old_instance.order_number is not None
            ):
                if self.order_number < old_instance.order_number:
                    Resource.objects.filter(
                        order_number__gte=self.order_number,
                        order_number__lt=old_instance.order_number,
                    ).update(order_number=models.F("order_number") + 1)
                else:
                    Resource.objects.filter(
                        order_number__gt=old_instance.order_number,
                        order_number__lte=self.order_number,
                    ).update(order_number=models.F("order_number") - 1)

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("Resurs")
        verbose_name_plural = _("Resurslar")
        ordering = ["order_number"]
