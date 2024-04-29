from django.db import models
from django.utils.translation import gettext_lazy as __


class Plan(models.Model):
    classes = models.ForeignKey("Classes", on_delete=models.CASCADE)
    topic = models.ForeignKey("Topic", on_delete=models.CASCADE)
    hour = models.IntegerField(default=0)

    def __str__(self):
        return self.topic.id

    class Meta:
        unique_together = (('topic', 'classes'),)
        verbose_name = __('Plan')
        verbose_name_plural = __('Plan')
