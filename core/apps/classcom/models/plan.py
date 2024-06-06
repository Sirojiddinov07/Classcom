from django.db import models
from django.utils.translation import gettext_lazy as __

from core.http.models import User


class Plan(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    banner = models.ImageField(upload_to="plan/banner/", blank=True, null=True)
    type = models.ForeignKey("ResourceType", on_delete=models.CASCADE, null=True, blank=True)
    hour = models.IntegerField(default=0, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    classes = models.ForeignKey("Classes", on_delete=models.CASCADE)
    quarter = models.ForeignKey("Quarter", on_delete=models.CASCADE)
    science = models.ForeignKey("Science", on_delete=models.CASCADE)
    topic = models.ForeignKey("Topic", on_delete=models.CASCADE)
    plan_resource = models.ForeignKey("Media", on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.topic.id

    class Meta:
        unique_together = (("topic", "classes"),)
        verbose_name = __("Plan")
        verbose_name_plural = __("Plan")
