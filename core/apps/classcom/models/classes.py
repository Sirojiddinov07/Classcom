from django.db import models
from django.utils.translation import gettext_lazy as __


class ClassType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = __("ClassType")
        verbose_name_plural = __("ClassTypes")


class Classes(models.Model):
    name = models.CharField(max_length=255)
    type = models.ForeignKey(
        ClassType, on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = __("Classes")
        verbose_name_plural = __("Classes")
