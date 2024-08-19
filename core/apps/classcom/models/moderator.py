from django.db import models
from django.utils.translation import gettext_lazy as __

from core.apps.classcom import choices
from core.apps.classcom.choices import Role
from core.apps.classcom.models.science import ScienceTypes
from core.http.models import AbstractBaseModel


class Moderator(AbstractBaseModel):
    user = models.OneToOneField(
        "http.User", on_delete=models.CASCADE, verbose_name=__("Foydalanuvchi")
    )
    balance = models.BigIntegerField(default=0, verbose_name=__("Balans"))
    science = models.ForeignKey(
        to="Science",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=__("Fan"),
    )
    science_type = models.ForeignKey(
        ScienceTypes,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=__("Fan turi"),
    )
    degree = models.CharField(
        max_length=15,
        choices=choices.Degree.choices,
        default=choices.Degree.AUTHOR,
        verbose_name=__("Daraja"),
    )
    docs = models.FileField(
        upload_to="documents/",
        null=True,
        blank=True,
        verbose_name=__("Hujjat"),
    )
    is_contracted = models.BooleanField(
        default=False, verbose_name=__("Shartnoma")
    )
    plan_creatable = models.BooleanField(
        default=True, verbose_name=__("Tematik Reja yarata olishi")
    )
    resource_creatable = models.BooleanField(
        default=True, verbose_name=__("Resurs yarata olishi.")
    )

    def __str__(self) -> str:
        return str(self.user.first_name)

    class Meta:
        verbose_name = __("Moderator")
        verbose_name_plural = __("Moderatorlar")

    def save(self, *args, **kwargs):
        if self.user.role != Role.MODERATOR:
            self.user.role = Role.MODERATOR
            self.user.save()
        super().save(*args, **kwargs)

    def get_dirty_fields(self):
        dirty_fields = {}
        if not self.pk:
            return dirty_fields

        db_instance = type(self).objects.get(pk=self.pk)
        for field in self._meta.fields:
            field_name = field.name
            if getattr(db_instance, field_name) != getattr(self, field_name):
                dirty_fields[field_name] = getattr(self, field_name)
        return dirty_fields


class TempModerator(AbstractBaseModel):
    user = models.OneToOneField(
        "http.User", on_delete=models.CASCADE, verbose_name=__("Foydalanuvchi")
    )
    balance = models.BigIntegerField(default=0, verbose_name=__("Balans"))
    science = models.ForeignKey(
        to="Science",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=__("Fan"),
    )
    science_type = models.ForeignKey(
        ScienceTypes,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=__("Fan turi"),
    )
    degree = models.CharField(
        max_length=15,
        choices=choices.Degree.choices,
        default=choices.Degree.AUTHOR,
        verbose_name=__("Daraja"),
    )
    docs = models.FileField(
        upload_to="documents/",
        null=True,
        blank=True,
        verbose_name=__("Hujjat"),
    )
    is_contracted = models.BooleanField(
        default=False, verbose_name=__("Shartnoma")
    )
