from django.db import models
from django.utils.translation import gettext_lazy as __

from core.http.models import User
from core.apps.classcom import choices


class Moderator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.BigIntegerField(default=0)
    science = models.ForeignKey(
        to="Science", on_delete=models.SET_NULL, null=True
    )
    classes = models.ForeignKey(
        to="Classes", on_delete=models.SET_NULL, null=True
    )
    degree = models.CharField(
        max_length=15,
        choices=choices.Degree.choices,
        default=choices.Degree.AUTHOR,
    )
    docs = models.FileField(upload_to='documents/', null=True, blank=True)
    is_contracted = models.BooleanField(default=False)

    def __str__(self) -> str:
        return str(self.user.first_name)

    class Meta:
        verbose_name = __("Moderator")
        verbose_name_plural = __("Moderators")

        

    def save(self, *args, **kwargs):
        if self.user.role != RoleChoice.ADMIN:
            self.user.role = RoleChoice.ADMIN
            self.user.save()
        super().save(*args, **kwargs)