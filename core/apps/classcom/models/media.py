from django.db import models
from django.utils.translation import gettext_lazy as __


class Media(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='media/')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = __("Media")
        verbose_name_plural = __("Medias")
