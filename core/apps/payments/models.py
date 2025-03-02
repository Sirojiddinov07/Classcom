from django.db import models
from django.utils.translation import gettext_lazy as _

from core.apps.classcom.models import Quarter
from core.apps.classcom.models.science import Science, ScienceTypes
from core.http.models import AbstractBaseModel
from core.http.models.school_group import ClassGroup


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
    class_type = models.ForeignKey(
        ClassGroup,
        on_delete=models.CASCADE,
        verbose_name=_("Sinf turi"),
    )
    price = models.BigIntegerField(default=0, verbose_name=_("Narxi"))
    status = models.BooleanField(default=False, verbose_name=_("Holati"))

    class Meta:
        verbose_name = _("Buyurtmalar")
        verbose_name_plural = _("Buyurtmalar")

    def __str__(self) -> str:
        if (
            self.user
            and self.user.region
            and self.user.district
            and self.science
        ):
            return (
                f"{self.id} {self.user.last_name} {self.user.first_name} "
                f"{self.user.father_name} - {self.science.name} {self.user.region.region} "
                f"{self.user.district.district} {self.user.role}"
            )
        return f"{self.id} - Incomplete User Information"


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
        if (
            self.order.user
            and self.order.user.region
            and self.order.user.district
            and self.order.science
        ):
            return (
                f"{self.id} {self.order.user.last_name} {self.order.user.first_name} "
                f"{self.order.user.father_name} - {self.order.science.name} {self.order.user.region.region} "
                f"{self.order.user.district.district} {self.order.user.role}"
            )
        return f"{self.id} - Incomplete User Information"


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
