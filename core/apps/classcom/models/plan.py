from django.db import models
from django.utils.translation import gettext_lazy as __


class Plan(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    banner = models.ImageField(upload_to="plan/banner/")
    type = models.ForeignKey(
        "ResourceType", on_delete=models.CASCADE, null=True, blank=True
    )
    hour = models.IntegerField(default=0, null=True, blank=True)
    user = models.ForeignKey("http.User", on_delete=models.CASCADE)
    classes = models.ForeignKey("Classes", on_delete=models.CASCADE)
    quarter = models.ForeignKey("Quarter", on_delete=models.CASCADE)
    science = models.ForeignKey("Science", on_delete=models.CASCADE)
    plan_resource = models.ManyToManyField("Media", blank=True)
    topic = models.ForeignKey(
        "Topic",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="plans",
    )
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = __("Plan")
        verbose_name_plural = __("Plan")
