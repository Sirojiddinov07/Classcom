from django.db import models
from core.apps.classcom import choices
from django.utils.translation import gettext_lazy as __

from core.http.models import User


from django.core.exceptions import ValidationError


def validate_lesson_time(value):
    try:
        lesson_time = int(value)
        if lesson_time <= 0 or lesson_time >= 7:
            raise ValidationError(
                f"Lesson time must be greater than 0 and less than 7. Given value: {value}"
            )
    except ValueError:
        raise ValidationError(
            f"Lesson time must be an integer. Given value: {value}"
        )


class Schedule(models.Model):
    shift = models.CharField(
        max_length=255,
        choices=choices.ShiftChoice.choices,
        default=choices.ShiftChoice.MORNING,
    )
    user = models.ForeignKey(User, models.CASCADE, related_name="schedules")
    science = models.ForeignKey("Science", models.CASCADE)
    classes = models.ForeignKey("Classes", models.CASCADE)
    weekday = models.CharField(max_length=15, choices=choices.Weekday.choices)
    start_time = models.TimeField()
    end_time = models.TimeField()
    lesson_time = models.CharField(
        max_length=25, validators=[validate_lesson_time]
    )
    quarter = models.ForeignKey("Quarter", models.CASCADE)

    def __str__(self):
        return f"{self.user} {self.science} {self.start_time} {self.end_time}"

    class Meta:
        verbose_name = __("Schedule")
        verbose_name_plural = __("Schedules")
