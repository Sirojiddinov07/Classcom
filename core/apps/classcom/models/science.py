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
        if not self.order_number:
            max = Science.objects.all().order_by("-order_number").first()
            if max:
                self.order_number = max.order_number + 1
            else:
                self.order_number = 1
        else:
            self.order_number = self.order_number
            for i in Science.objects.filter(
                order_number__gte=self.order_number
            ):
                i.order_number += 1
                i.save()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("Fan")
        verbose_name_plural = _("Fanlar")
