from django.db import models
from django.utils.translation import gettext as _
from core.apps.classcom.models.science import Science, ScienceTypes


class Orders(models.Model):
    user = models.ForeignKey("http.User", on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    science = models.ForeignKey(Science, on_delete=models.CASCADE)
    types = models.ManyToManyField(ScienceTypes)
    price = models.BigIntegerField(default=0)
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Orders")
        verbose_name_plural = _("Orderss")

    def __str__(self):
        return self.user.first_name or self.id
