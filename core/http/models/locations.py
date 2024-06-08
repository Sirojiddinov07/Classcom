from django.db import models
from django.utils.translation import gettext_lazy as _


class Region(models.Model):
    region = models.CharField(max_length=255)

    def __str__(self):
        return self.region


class District(models.Model):
    district = models.CharField(max_length=255)
    region = models.ForeignKey(
        "Region", on_delete=models.CASCADE, related_name="districts"
    )

    def __str__(self):
        return self.district
