from django.db import models
from django.utils.translation import gettext as _

from core.apps.classcom.models import Quarter
from core.apps.classcom.models.science import Science, ScienceTypes
from core.http.models import AbstractBaseModel


class Orders(AbstractBaseModel):
    """Order Model"""

    user = models.ForeignKey(
        "http.User",
        on_delete=models.CASCADE,
        related_name="orders",
        verbose_name=_("Foydalanuvchi"),
    )
    start_date = models.DateField(
        auto_now_add=True,
        blank=True,
        null=True,
        verbose_name=_("Boshlanish sanasi"),
    )
    end_date = models.DateField(
        blank=True, null=True, verbose_name=_("Tugash sanasi")
    )
    science = models.ForeignKey(
        Science, on_delete=models.CASCADE, verbose_name=_("Fan")
    )
    types = models.ManyToManyField(ScienceTypes, verbose_name=_("Fan turi"))
    price = models.BigIntegerField(default=0, verbose_name=_("Narxi"))
    status = models.BooleanField(default=False, verbose_name=_("Holati"))

    class Meta:
        verbose_name = _("Buyurtmalar")
        verbose_name_plural = _("Buyurtmalar")

    def __str__(self) -> str:
        return f"{self.id} {self.user.first_name}"


class Payments(AbstractBaseModel):
    order = models.ForeignKey(
        Orders,
        on_delete=models.CASCADE,
        related_name="payments",
        verbose_name=_("Buyurtma"),
    )
    price = models.BigIntegerField(default=0, verbose_name=_("Narxi"))
    status = models.BooleanField(default=False, verbose_name=_("Holati"))
    trans_id = models.CharField(
        max_length=255, unique=True, verbose_name=_("Tranzaksiya ID")
    )

    class Meta:
        verbose_name = _("Payments")
        verbose_name_plural = _("Payments")

    def __str__(self) -> str:
        return f"{self.id} {self.order.id}"


class Plans(AbstractBaseModel):
    quarter = models.ForeignKey(
        Quarter, on_delete=models.CASCADE, verbose_name=_("Chorak")
    )
    price = models.BigIntegerField(default=0, verbose_name=_("Narxi"))

    class Meta:
        verbose_name = _("Reja")
        verbose_name_plural = _("Rejalar")

    def __str__(self):
        return f"{self.price}"
