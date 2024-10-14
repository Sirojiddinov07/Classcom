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


class ChangeModerator(AbstractBaseModel):
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
    science = models.ForeignKey(
        to="Science",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Fan"),
    )
    science_type = models.ManyToManyField(
        ScienceTypes,
        blank=True,
        verbose_name=_("Fan turi"),
    )
    classes = models.ForeignKey(
        Classes,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Sinflar"),
    )
    class_groups = models.ForeignKey(
        ClassGroup,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Sinflar turlari"),
    )

    def __str__(self):
        return f"{self.user} - {self.status}"

    class Meta:
        verbose_name = _("Moderatorni arizasi")
        verbose_name_plural = _("Moderator arizalari")
        ordering = ("-created_at",)

    @classmethod
    def get_pending(cls):
        return cls.objects.filter(status=ChangeModeratorStatus.PENDING).count()
