from django.db import models
from ..choices import Types


class ResourceType(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(choices=Types.choices)

    def __str__(self):
        return self.name
