from django.db import models
from django.utils.translation import gettext_lazy as __
from ..choices import Types, ResourceDegree


class Resource(models.Model):
    category = models.ForeignKey(
        "Category", on_delete=models.CASCADE, null=True, blank=True
    )
    category_type = models.ForeignKey(
        "CategoryType", on_delete=models.CASCADE, null=True, blank=True
    )
    name = models.CharField(max_length=255)
    description = models.TextField()

    banner = models.ImageField(upload_to="resource_banners/")
    type = models.ForeignKey(
        "ResourceType", on_delete=models.CASCADE, null=True, blank=True
    )
    subtype = models.CharField(max_length=255, null=True, blank=True)

    user = models.ForeignKey("http.User", on_delete=models.CASCADE)
    classes = models.ForeignKey(
        "Classes", on_delete=models.CASCADE, null=True, blank=True
    )
    media = models.ManyToManyField(
        "Media", blank=True, related_name="resources"
    )
    source = models.CharField(max_length=255, null=True, blank=True)
    degree = models.CharField(
        choices=ResourceDegree.choices, default=ResourceDegree.MEDIUM
    )

    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return str(self.name) or "Unnamed Resource"

    class Meta:
        verbose_name = __("Resource")
        verbose_name_plural = __("Resources")


class ResourceTypes(models.Model):
    name = models.CharField()
    type = models.CharField(choices=Types.choices)
