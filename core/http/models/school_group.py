from django.db import models
from django.utils.translation import gettext_lazy as _

from core.apps.classcom.models import Science
from core.http.models import AbstractBaseModel, SchoolType


class ClassGroup(AbstractBaseModel):
    name = models.CharField(max_length=255, verbose_name=_("Sinf turi"))
    school_type = models.ForeignKey(
        SchoolType,
        on_delete=models.CASCADE,
        related_name="class_groups",
        verbose_name=_("Maktab turi"),
    )
    science = models.ForeignKey(
        Science,
        on_delete=models.CASCADE,
        related_name="class_groups",
        verbose_name=_("Fan"),
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Sinf turi")
        verbose_name_plural = _("Sinf turlari")
