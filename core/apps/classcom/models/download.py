from django.db import models
from core.apps.classcom import models as md
from django.utils.translation import gettext_lazy as __


class Download(models.Model):
    teacher = models.ForeignKey(md.Teacher, on_delete=models.CASCADE)
    date = models.DateField()
    resource = models.ForeignKey(md.Resource, on_delete=models.CASCADE)

    def __str__(self):
        return super().__str__()

    class Meta:
        verbose_name = __("Download")
        verbose_name_plural = __("Downloads")
