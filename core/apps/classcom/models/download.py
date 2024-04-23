from django.db import models
from django.utils.translation import gettext_lazy as __


class Download(models.Model):
    teacher = models.ForeignKey("Teacher", on_delete=models.CASCADE)
    date = models.DateField()
    resource = models.ForeignKey("Resource", on_delete=models.CASCADE)

    def __str__(self):
        return super().__str__()

    class Meta:
        verbose_name = __("Download")
        verbose_name_plural = __("Downloads")
