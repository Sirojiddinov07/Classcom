from django.db import models
from core.apps.classcom import choices
from django.utils.translation import gettext_lazy as __

from core.http.models import User


class Schedule(models.Model):
    shift = models.CharField(max_length=255, choices=choices.ShiftChoice.choices, default=choices.ShiftChoice.MORNING)
    teacher = models.ForeignKey(User, models.CASCADE)
    science = models.ForeignKey("Science", models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.teacher} {self.science} {self.start_time} {self.end_time}"

    class Meta:
        verbose_name = __("Schedule")
        verbose_name_plural = __("Schedules")
