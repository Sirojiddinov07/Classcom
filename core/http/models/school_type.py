from django.db import models


class SchoolType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "SchoolType"
        verbose_name_plural = "SchoolTypes"
