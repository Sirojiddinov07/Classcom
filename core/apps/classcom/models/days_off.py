from django.db import models


class DaysOff(models.Model):
    from_date = models.DateField()
    to_date = models.DateField()
    reason = models.CharField(max_length=255)
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
