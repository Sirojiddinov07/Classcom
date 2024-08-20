from django.db import models
from django.utils.translation import gettext_lazy as _

from core.http.models import AbstractBaseModel


class ClassType(AbstractBaseModel):
    name = models.CharField(max_length=255, verbose_name=_("Sinf turi"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Sinf turi")
        verbose_name_plural = _("Sinf turlari")


class Classes(AbstractBaseModel):
    name = models.CharField(max_length=255, verbose_name=_("Sinf nomi"))
    type = models.ForeignKey(
        ClassType,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=_("Sinf turi"),
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Sinf")
        verbose_name_plural = _("Sinflar")
