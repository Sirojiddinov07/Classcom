from django.db import models
from . import science, classes


class DaysOff(models.Model):
    from_date = models.DateField()
    to_date = models.DateField()
    reason = models.CharField(max_length=255)
    science = models.ManyToManyField(science.Science)
    _class = models.ManyToManyField(classes.Classes)
    user = models.ForeignKey(
        "http.User",
        on_delete=models.CASCADE,
        related_name="days_off",
        null=True,
        blank=True,
    )

    class Meta:
        db_table = "days_off"

    def __str__(self):
        return self.reason
