from django.db import models
from django.utils.translation import gettext_lazy as __


class Settings(models.Model):
    key = models.CharField(max_length=255, unique=True)
    value = models.TextField()

    def __str__(self):
        return self.key

    class Meta:
        verbose_name = __("Settings")
        verbose_name_plural = __("Settings")
