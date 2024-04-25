from django.db import models
from django.utils.translation import gettext_lazy as __

from core.http.models import User


class Teacher(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    science = models.ManyToManyField("Science", blank=True)

    def __str__(self):
        return self.user.first_name

    class Meta:
        verbose_name = __("Teacher")
        verbose_name_plural = __("Teachers")
