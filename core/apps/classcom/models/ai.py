from django.db import models
from django.utils.translation import gettext_lazy as _

from core.apps.classcom.models import Topic
from core.http.models import AbstractBaseModel


class Ai(AbstractBaseModel):
    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        related_name="ais",
        verbose_name=_("Mavzu"),
    )
    user = models.ForeignKey(
        "http.User",
        on_delete=models.CASCADE,
        related_name="ais",
        verbose_name=_("Foydalanuvchi"),
    )
    question = models.TextField(verbose_name=_("Savol"))
    answer = models.TextField(verbose_name=_("Javob"))

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = _("Suniy Intellekt")
        verbose_name_plural = _("Suniy Intellektlar")
