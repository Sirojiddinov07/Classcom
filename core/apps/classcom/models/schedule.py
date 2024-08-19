import datetime

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.apps.classcom import choices
from core.http.models import AbstractBaseModel


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


class Schedule(AbstractBaseModel):
    shift = models.CharField(
        max_length=255,
        choices=choices.ShiftChoice.choices,
        default=choices.ShiftChoice.MORNING,
        verbose_name=_("Smena"),
    )
    user = models.ForeignKey(
        "http.User",
        models.CASCADE,
        related_name="schedules",
        verbose_name=_("Foydalanuvchi"),
    )
    science = models.ForeignKey(
        "Science", models.CASCADE, verbose_name=_("Fan")
    )
    classes = models.ForeignKey(
        "Classes", models.CASCADE, verbose_name=_("Sinflar")
    )
    weekday = models.CharField(
        max_length=15,
        choices=choices.Weekday.choices,
        null=True,
        blank=True,
        verbose_name=_("Kun"),
    )
    start_time = models.TimeField(verbose_name=_("Boshlanish vaqti"))
    end_time = models.TimeField(verbose_name=_("Tugash vaqti"))
    lesson_time = models.CharField(
        max_length=25,
        validators=[validate_lesson_time],
        verbose_name=_("Dars vaqti"),
    )
    quarter = models.ForeignKey(
        "Quarter", models.CASCADE, verbose_name=_("Chorak")
    )
    date = models.DateField(verbose_name=_("Sana"))

    def __str__(self):
        return f"{self.user} {self.science} {self.start_time} {self.end_time}"

    class Meta:
        verbose_name = _("Dars jadvali")
        verbose_name_plural = _("Dars jadvali")
        unique_together = ("date", "start_time", "end_time", "user")

    def save(self, *args, **kwargs):
        weekday_map = {
            "Monday": choices.Weekday.monday,
            "Tuesday": choices.Weekday.tuesday,
            "Wednesday": choices.Weekday.wednesday,
            "Thursday": choices.Weekday.thursday,
            "Friday": choices.Weekday.friday,
            "Saturday": choices.Weekday.saturday,
        }
        if isinstance(self.date, datetime.date):
            date_str = self.date.isoformat()
        else:
            date_str = self.date

        if datetime.date.fromisoformat(date_str).strftime("%A") == "Sunday":
            raise ValidationError("Date cannot be Sunday.")
        self.weekday = weekday_map[
            datetime.date.fromisoformat(date_str).strftime("%A")
        ]
        super().save(*args, **kwargs)
