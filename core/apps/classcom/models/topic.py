from django.db import models
from core.apps.classcom import models as md
from django.utils.translation import gettext_lazy as __


class Topic(models.Model):
    name = models.CharField(max_length=255)
    quarter = models.ForeignKey(md.Quarter, on_delete=models.CASCADE)
    science = models.ForeignKey(md.Science, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = __("Topic")
        verbose_name_plural = __("Topics")
