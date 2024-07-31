from django.db import models
from django.utils.translation import gettext_lazy as __


class Resource(models.Model):
    category = models.ForeignKey("Category", on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)
    description = models.TextField()

    banner = models.ImageField(upload_to="resource_banners/")
    type = models.ForeignKey(
        "ResourceType", on_delete=models.CASCADE, null=True, blank=True
    )

    user = models.ForeignKey("http.User", on_delete=models.CASCADE)
    classes = models.ForeignKey(
        "Classes", on_delete=models.CASCADE, null=True, blank=True
    )
    media = models.ManyToManyField(
        "Media", blank=True, related_name="resources"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = __("Resource")
        verbose_name_plural = __("Resources")
