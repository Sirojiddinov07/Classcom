from django.db import models
from django.utils.translation import gettext_lazy as __


class Topic(models.Model):
    name = models.CharField(max_length=255)
    quarter = models.ForeignKey("Quarter", on_delete=models.CASCADE)
    science = models.ForeignKey("Science", on_delete=models.CASCADE)
    thematic_plan = models.ForeignKey("Plan", on_delete=models.CASCADE, null=True, blank=True, related_name="topics")  # Added related_name


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = __("Topic")
        verbose_name_plural = __("Topics")
