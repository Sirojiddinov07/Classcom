from datetime import datetime

from django.db import models
from django.utils.translation import gettext_lazy as __


class Quarter(models.Model):
    Q1 = 1
    Q2 = 2
    Q3 = 3
    Q4 = 4

    QUARTER_CHOICES = [
        (Q1, "First Quarter"),
        (Q2, "Second Quarter"),
        (Q3, "Third Quarter"),
        (Q4, "Fourth Quarter"),
    ]

    choices = models.IntegerField(
        choices=QUARTER_CHOICES,
        default=Q1,
    )
    start_date = models.DateField(default=datetime.today, blank=True)
    end_date = models.DateField(default=datetime.today, blank=True)

    def __str__(self):
        return f" {self.choices} ({self.start_date} - {self.end_date})"

    class Meta:
        verbose_name = __("Quarter")
        verbose_name_plural = __("Quarters")
