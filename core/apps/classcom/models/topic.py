from django.db import models
from django.utils.translation import gettext_lazy as __
from django.db.models.signals import post_save
from django.dispatch import receiver

from core.apps.classcom.models import Plan


class Topic(models.Model):
    name = models.CharField(max_length=255)
    quarter = models.ForeignKey("Quarter", on_delete=models.CASCADE)
    science = models.ForeignKey("Science", on_delete=models.CASCADE)
    _class = models.ForeignKey("Classes", on_delete=models.CASCADE)
    sequence_number = models.IntegerField(default=1)
    thematic_plan = models.ManyToManyField(
        "Plan",
        null=True,
        blank=True,
        related_name="topics",
    )  # Added related_name

    def __str__(self):
        return f"{self.name}, {self.id}"

    class Meta:
        verbose_name = __("Topic")
        verbose_name_plural = __("Topics")
        unique_together = ("sequence_number", "science", "_class")


@receiver(post_save, sender=Plan)
def add_plan_to_thematic_plan(sender, instance, created, **kwargs):
    if instance.topic and created:
        instance.topic.thematic_plan.add(instance)