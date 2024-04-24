from django.db import models
from core.apps.classcom import models as md
from django.utils.translation import gettext_lazy as __


class Resource(models.Model):
    name = models.CharField(max_length=255)
    desc = models.TextField()

    topic = models.ForeignKey(md.Topic, on_delete=models.CASCADE)
    moderator = models.ForeignKey(md.Moderator, on_delete=models.CASCADE)
    classes = models.ForeignKey(md.Classes, on_delete=models.CASCADE)

    media = models.ManyToManyField(md.Media, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = __("Resource")
        verbose_name_plural = __("Resources")
