from django.db import models
from django.utils.translation import gettext as _
from core.apps.classcom.models.science import Science, ScienceTypes
from core.apps.classcom.models import Quarter


class Orders(models.Model):
    """Order Model"""

    user = models.ForeignKey("http.User", on_delete=models.CASCADE)
    start_date = models.DateField(auto_now_add=True, blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    science = models.ForeignKey(Science, on_delete=models.CASCADE)
    types = models.ManyToManyField(ScienceTypes)
    price = models.BigIntegerField(default=0)
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Orders")
        verbose_name_plural = _("Orders")

    def __str__(self) -> str:
        return f"{self.id} {self.user.first_name}"


class Payments(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    price = models.BigIntegerField(default=0)
    status = models.BooleanField(default=False)
    trans_id = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Payments")
        verbose_name_plural = _("Payments")

    def __str__(self) -> str:
        return f"{self.id} {self.order.id}"


class Plans(models.Model):
    quarter = models.ForeignKey(Quarter, on_delete=models.CASCADE)
    price = models.BigIntegerField(default=0)

    class Meta:
        verbose_name = _("Plans")
        verbose_name_plural = _("Plans")

    def __str__(self):
        return f"{self.price}"
