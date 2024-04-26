from django.db import models
from django.utils.translation import gettext_lazy as __


class Media(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='media/')
    type = models.CharField(max_length=255, blank=True, null=True)
    size = models.BigIntegerField(blank=True, null=True, default=0)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = __("Media")
        verbose_name_plural = __("Medias")
