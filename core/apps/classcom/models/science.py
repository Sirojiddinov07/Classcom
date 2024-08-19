from django.db import models
from django.utils.translation import gettext_lazy as __

from core.http.models import ScienceGroups, AbstractBaseModel


class ScienceTypes(AbstractBaseModel):
    name = models.CharField(verbose_name=__("Name"))

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = __("Fan turi")
        verbose_name_plural = __("Fan turlari")


class Science(AbstractBaseModel):
    name = models.CharField(verbose_name=__("Nomi"))
    science_grp = models.ForeignKey(
        ScienceGroups,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=__("Fan guruhi"),
    )
    types = models.ManyToManyField(ScienceTypes, verbose_name=__("Fan turi"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = __("Fan")
        verbose_name_plural = __("Fanlar")
