from django.db import models
from django.utils.translation import gettext_lazy as _

from core.http.models import AbstractBaseModel
from ..choices import Types, ResourceDegree


class Resource(AbstractBaseModel):
    category = models.ForeignKey(
        "Category",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=_("Kategoriya"),
    )
    category_type = models.ForeignKey(
        "CategoryType",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=_("Kategoriya turi"),
    )
    name = models.CharField(max_length=255, verbose_name=_("Nomi"))
    description = models.TextField(verbose_name=_("Tavsif"))

    banner = models.ImageField(
        upload_to="resource_banners/", verbose_name=_("Banner")
    )
    type = models.ForeignKey(
        "ResourceType",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=_("Resurs turi"),
    )
    subtype = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Resurs sub turi"),
    )

    user = models.ForeignKey(
        "http.User", on_delete=models.CASCADE, verbose_name=_("Foydalanuvchi")
    )
    classes = models.ForeignKey(
        "Classes",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=_("Sinflar"),
    )
    media = models.ManyToManyField(
        "Media", blank=True, related_name="resources", verbose_name=_("Media")
    )
    source = models.CharField(
        max_length=255, null=True, blank=True, verbose_name=_("Manba")
    )
    degree = models.CharField(
        choices=ResourceDegree.choices,
        default=ResourceDegree.MEDIUM,
        verbose_name=_("Daraja"),
    )

    def __str__(self):
        return str(self.name) or "Unnamed Resource"

    class Meta:
        verbose_name = _("Resurs")
        verbose_name_plural = _("Resurslar")


class ResourceTypes(AbstractBaseModel):
    name = models.CharField(verbose_name=_("Nomi"), max_length=255)
    type = models.CharField(
        choices=Types.choices, verbose_name=_("Turi"), max_length=255
    )
