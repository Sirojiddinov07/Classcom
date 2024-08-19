from django.db import models
from django.utils.translation import gettext_lazy as _

from core.http.models import AbstractBaseModel
from . import classes, science


class DaysOff(AbstractBaseModel):
    from_date = models.DateField(verbose_name=_("Boshlang'ich sana"))
    to_date = models.DateField(verbose_name=_("Oxirgi sana"))
    reason = models.CharField(max_length=255, verbose_name=_("Sababi"))
    science = models.ManyToManyField(science.Science, verbose_name=_("Fanlar"))
    _class = models.ManyToManyField(classes.Classes, verbose_name=_("Sinflar"))
    user = models.ForeignKey(
        "http.User",
        on_delete=models.CASCADE,
        related_name="days_off",
        null=True,
        blank=True,
        verbose_name=_("Foydalanuvchi"),
    )

    class Meta:
        db_table = "days_off"
        verbose_name = _("Dam olish kuni")
        verbose_name_plural = _("Dam olish kunlari")

    def __str__(self):
        return self.reason
