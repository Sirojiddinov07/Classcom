from django.db import models
from django.utils.translation import gettext_lazy as _

from core.apps.classcom import choices
from core.apps.classcom.models import Classes
from core.apps.classcom.models.science import ScienceTypes
from core.http.models import AbstractBaseModel
from core.http.models.school_group import ClassGroup


class Moderator(AbstractBaseModel):
    user = models.OneToOneField(
        "http.User", on_delete=models.CASCADE, verbose_name=_("Foydalanuvchi")
    )
    balance = models.BigIntegerField(default=0, verbose_name=_("Balans"))
    degree = models.CharField(
        max_length=15,
        choices=choices.Degree,
        default=choices.Degree.AUTHOR,
        verbose_name=_("Daraja"),
    )
    docs = models.ManyToManyField(
        "Document",
        blank=True,
        related_name="moderators",
        verbose_name=_("Hujjatlar"),
    )
    is_contracted = models.BooleanField(
        default=False, verbose_name=_("Tasdiqlash")
    )
    status = models.BooleanField(
        default=False, verbose_name=_("Shartnoma statusi")
    )
    ##############
    # Permissions
    ##############
    plan_creatable = models.BooleanField(
        default=False, verbose_name=_("Tematik Reja yarata olishi")
    )
    resource_creatable = models.BooleanField(
        default=False, verbose_name=_("Resurs yarata olishi.")
    )
    topic_creatable = models.BooleanField(
        default=False, verbose_name=_("Mavzu yarata olishi.")
    )
    resource_type = models.ManyToManyField(
        "ResourceType",
        blank=True,
        related_name="moderators",
        verbose_name=_("Resurs turlari"),
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
    languages = models.ManyToManyField(
        "LanguageModel",
        blank=True,
        related_name="moderators",
        verbose_name=_("Tillar"),
    )
    classes = models.ManyToManyField(
        Classes,
        blank=True,
        related_name="moderators",
        verbose_name=_("Sinflar"),
    )
    class_groups = models.ManyToManyField(
        ClassGroup,
        blank=True,
        related_name="moderators",
        verbose_name=_("Sinflar turlari"),
    )
    quarters = models.ManyToManyField(
        "Quarter",
        blank=True,
        related_name="moderators",
        verbose_name=_("Choraklar"),
    )

    def __str__(self) -> str:
        return (
            f"{self.user.first_name} {self.user.last_name} | {self.user.phone}"
        )

    @classmethod
    def moderator_get_status_count(cls):
        return cls.objects.filter(is_contracted=False).count()

    class Meta:
        verbose_name = _("Moderator")
        verbose_name_plural = _("Moderatorlar")
        ordering = ["-updated_at"]
