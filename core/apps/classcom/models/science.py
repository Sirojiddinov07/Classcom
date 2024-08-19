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

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Fan")
        verbose_name_plural = _("Fanlar")
