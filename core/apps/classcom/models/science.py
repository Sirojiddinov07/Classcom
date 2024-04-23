from django.db import models
from django.utils.translation import gettext_lazy as __


class Science(models.Model):
    name = models.CharField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = __("Science")
        verbose_name_plural = __("Sciences")