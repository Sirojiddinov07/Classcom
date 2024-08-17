from django.db import models
from django.utils.translation import gettext_lazy as __


class Download(models.Model):
    teacher = models.ForeignKey(
        "Teacher", on_delete=models.CASCADE, blank=True, null=True
    )
    moderator = models.ForeignKey(
        "Moderator", on_delete=models.CASCADE, blank=True, null=True
    )
    date = models.DateField()
    media = models.ForeignKey("Media", on_delete=models.CASCADE)

    def __str__(self):
        return super().__str__()

    class Meta:
        verbose_name = __("Download")
        verbose_name_plural = __("Downloads")
