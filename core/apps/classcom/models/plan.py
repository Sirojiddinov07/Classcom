from django.db import models
from django.utils.translation import gettext_lazy as _

from core.http.models import AbstractBaseModel


class Plan(AbstractBaseModel):
    name = models.CharField(max_length=255, verbose_name=_("Nomi"))
    description = models.TextField(verbose_name=_("Tavsif"))

    banner = models.ImageField(
        upload_to="plan/banner/", verbose_name=_("Banner")
    )
    type = models.ForeignKey(
        "ResourceType",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=_("Resurs turi"),
    )
    hour = models.IntegerField(
        default=0, null=True, blank=True, verbose_name=_("Soat")
    )
    user = models.ForeignKey(
        "http.User", on_delete=models.CASCADE, verbose_name=_("Foydalanuvchi")
    )
    classes = models.ForeignKey(
        "Classes", on_delete=models.CASCADE, verbose_name=_("Sinflar")
    )
    quarter = models.ForeignKey(
        "Quarter", on_delete=models.CASCADE, verbose_name=_("Chorak")
    )
    science = models.ForeignKey(
        "Science", on_delete=models.CASCADE, verbose_name=_("Fan")
    )
    plan_resource = models.ManyToManyField(
        "Media", blank=True, verbose_name=_("Resurslar")
    )
    # topic = models.ManyToManyField(
    #     "Topic",
    #     related_name="plans",
    #     verbose_name=_("Mavzu"),
    # )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Tematik reja")
        verbose_name_plural = _("Tematik rejalar")
