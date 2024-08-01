from django.db import models
from django.utils.translation import gettext_lazy as __

from core.http.models import ScienceGroups


class ScienceTypes(models.Model):
    name = models.CharField()


class Science(models.Model):
    name = models.CharField()
    science_grp = models.ForeignKey(
        ScienceGroups, on_delete=models.CASCADE, null=True
    )
    types = models.ManyToManyField(ScienceTypes)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = __("Science")
        verbose_name_plural = __("Sciences")
