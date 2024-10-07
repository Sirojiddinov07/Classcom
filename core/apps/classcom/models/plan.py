from django.db import models
from django.utils.translation import gettext_lazy as _

from core.apps.classcom.choices import Language
from core.apps.classcom.models.science import ScienceTypes
from core.http.models import AbstractBaseModel
from core.http.models.school_group import ClassGroup


class Plan(AbstractBaseModel):
    is_active = models.BooleanField(default=True, verbose_name=_("Faol"))
    hour = models.IntegerField(
        default=0, null=True, blank=True, verbose_name=_("Soat")
    )
    language = models.CharField(
        max_length=2,
        choices=Language.choices,
        default=Language.uz,
        verbose_name=_("Til"),
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
    # topic = models.ManyToManyField(
    #     "Topic",
    #     related_name="plans",
    #     verbose_name=_("Mavzu"),
    #     blank=True,
    # )
    class_group = models.ForeignKey(
        ClassGroup,
        on_delete=models.CASCADE,
        verbose_name=_("Sinflar guruhi"),
    )
    science_types = models.ForeignKey(
        ScienceTypes,
        on_delete=models.CASCADE,
        verbose_name=_("Fan guruhi"),
    )

    def __str__(self):
        return f"ID: {self.id}"

    def save(self, *args, **kwargs):
        if not self.pk:
            super().save(*args, **kwargs)

        self.hour = (
            self.topic.aggregate(models.Sum("hours"))["hours__sum"] or 0
        )

        super().save(update_fields=["hour"])

    class Meta:
        verbose_name = _("Tematik reja")
        verbose_name_plural = _("Tematik rejalar")
        unique_together = (
            "classes",
            "quarter",
            "science",
            "class_group",
            "science_types",
        )
