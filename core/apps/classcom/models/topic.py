from django.db import models
from django.utils.translation import gettext_lazy as __


class Topic(models.Model):
    name = models.CharField(max_length=255)
    quarter = models.ForeignKey("Quarter", on_delete=models.CASCADE)
    science = models.ForeignKey("Science", on_delete=models.CASCADE)
    _class = models.ForeignKey("Classes", on_delete=models.CASCADE)
    sequence_number = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.name}, {self.id}"

    class Meta:
        verbose_name = __("Topic")
        verbose_name_plural = __("Topics")
        unique_together = ("sequence_number", "science", "_class")
