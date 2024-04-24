from django.db import models
from core.apps.classcom import models as md
from django.utils.translation import gettext_lazy as __


class Teacher(models.Model):
    user = models.ForeignKey(md.User, on_delete=models.CASCADE)
    science = models.ManyToManyField(md.Science, blank=True)

    def __str__(self):
        return self.user.first_name

    class Meta:
        verbose_name = __("Teacher")
        verbose_name_plural = __("Teachers")
