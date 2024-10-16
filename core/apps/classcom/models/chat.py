from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from core.http.models import AbstractBaseModel


class Chat(AbstractBaseModel):
    user = models.ForeignKey(
        "http.User", on_delete=models.CASCADE, verbose_name=_("Foydalanuvchi")
    )
    massage = models.TextField(verbose_name=_("Xabar"))
    time = models.DateTimeField(auto_now_add=True, verbose_name=_("Vaqt"))
    response = models.TextField(null=True, blank=True, verbose_name=_("Javob"))
    response_time = models.DateTimeField(
        null=True, blank=True, verbose_name=_("Javob vaqti")
    )
    is_answered = models.BooleanField(
        default=False, verbose_name=_("Javob berildi")
    )

    @classmethod
    def get_unanswered(cls):
        return cls.objects.filter(is_answered=False).count()

    def __str__(self):
        return f"Chat by {self.user} to admin"

    def save(self, *args, **kwargs):
        if self.response:
            self.response_time = timezone.now()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("Chat")
        verbose_name_plural = _("Chatlar")
