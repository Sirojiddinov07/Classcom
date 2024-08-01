from django.db import models
from django.utils.translation import gettext_lazy as __


class Category(models.Model):
    name = models.CharField(max_length=255)
    category_type = models.ForeignKey("CategoryType", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = __("Category")
        verbose_name_plural = __("Categories")
