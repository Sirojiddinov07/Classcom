from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as __

from core.apps.classcom.models import Plan
from core.http.models import AbstractBaseModel


class Topic(AbstractBaseModel):
    name = models.CharField(max_length=255, verbose_name=__("Nomi"))
    quarter = models.ForeignKey(
        "Quarter", on_delete=models.CASCADE, verbose_name=__("Chorak")
    )
    science = models.ForeignKey(
        "Science", on_delete=models.CASCADE, verbose_name=__("Fan")
    )
    _class = models.ForeignKey(
        "Classes", on_delete=models.CASCADE, verbose_name=__("Sinflar")
    )
    sequence_number = models.IntegerField(
        default=1, verbose_name=__("Tartib raqami")
    )
    thematic_plan = models.ManyToManyField(
        "Plan",
        blank=True,
        related_name="topics",
        verbose_name=__("Tematik reja"),
    )

    def __str__(self):
        return f"{self.name}, {self.id}"

    class Meta:
        verbose_name = __("Mavzu")
        verbose_name_plural = __("Mavzular")
        unique_together = ("sequence_number", "science", "_class")


@receiver(post_save, sender=Plan)
def add_plan_to_thematic_plan(sender, instance, created, **kwargs):
    if instance.topic and created:
        instance.topic.thematic_plan.add(instance)
