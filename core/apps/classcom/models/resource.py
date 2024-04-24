from django.db import models
from django.utils.translation import gettext_lazy as __

from core.http.models import User


class Resource(models.Model):
    name = models.CharField(max_length=255)
    desc = models.TextField()

    topic = models.ForeignKey("Topic", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    classes = models.ForeignKey("Classes", on_delete=models.CASCADE)

    media = models.ManyToManyField("Media", blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = __("Resource")
        verbose_name_plural = __("Resources")
