from django.db import models
from django.utils.translation import gettext_lazy as _

from core.apps.classcom.models import Classes
from core.apps.classcom.models.science import ScienceTypes
from core.http.models import AbstractBaseModel
from core.http.models.school_group import ClassGroup


class ChangeModeratorStatus(models.TextChoices):
    PENDING = "pending", _("Kutilmoqda")
    ACCEPTED = "accepted", _("Qabul qilindi")
    REJECTED = "rejected", _("Rad etildi")


class PlanAppeal(AbstractBaseModel):
    user = models.ForeignKey(
        to="http.User",
        on_delete=models.CASCADE,
        verbose_name=_("Foydalanuvchi"),
    )
    status = models.CharField(
        max_length=20,
        choices=ChangeModeratorStatus.choices,
        default=ChangeModeratorStatus.PENDING,
        verbose_name=_("Holat"),
    )
    science = models.ManyToManyField(
        to="Science",
        blank=True,
        verbose_name=_("Fan"),
    )
    science_type = models.ManyToManyField(
        ScienceTypes,
        blank=True,
        verbose_name=_("Fan turi"),
    )
    classes = models.ManyToManyField(
        Classes,
        blank=True,
        verbose_name=_("Sinflar"),
    )
    class_groups = models.ManyToManyField(
        ClassGroup,
        blank=True,
        verbose_name=_("Sinflar turlari"),
    )
    tmr_files = models.ManyToManyField(
        "TmrFiles",
        blank=True,
        verbose_name=_("Fayllar"),
    )

    def __str__(self):
        return f"{self.user} - {self.status}"

    class Meta:
        verbose_name = _("TMR arizalari")
        verbose_name_plural = _("TMR arizalari")
        ordering = ("-created_at",)

    @classmethod
    def get_pending(cls):
        return cls.objects.filter(status=ChangeModeratorStatus.PENDING).count()
