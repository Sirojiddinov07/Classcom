from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from core.apps.classcom.models import Plan
from core.http.models import AbstractBaseModel


class Topic(AbstractBaseModel):
    name = models.CharField(max_length=255, verbose_name=_("Nomi"))
    quarter = models.ForeignKey(
        "Quarter", on_delete=models.CASCADE, verbose_name=_("Chorak")
    )
    science = models.ForeignKey(
        "Science", on_delete=models.CASCADE, verbose_name=_("Fan")
    )
    _class = models.ForeignKey(
        "Classes", on_delete=models.CASCADE, verbose_name=_("Sinflar")
    )
    sequence_number = models.IntegerField(
        default=1, verbose_name=_("Tartib raqami")
    )
    thematic_plan = models.ManyToManyField(
        "Plan",
        blank=True,
        related_name="topics",
        verbose_name=_("Tematik reja"),
    )

    def __str__(self):
        return f"{self.name}, {self.id}"

    class Meta:
        verbose_name = _("Mavzu")
        verbose_name_plural = _("Mavzular")
        unique_together = ("sequence_number", "science", "_class")


@receiver(post_save, sender=Plan)
def add_plan_to_thematic_plan(sender, instance, created, **kwargs):
    if instance.topic and created:
        instance.topic.thematic_plan.add(instance)
