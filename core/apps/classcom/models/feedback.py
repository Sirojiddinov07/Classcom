from django.core.validators import MaxLengthValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.http.choices.feedback import FeedbackType
from core.http.models.base import AbstractBaseModel


class Feedback(AbstractBaseModel):
    feedback_type = models.CharField(
        max_length=10,
        choices=FeedbackType.choices,
        verbose_name=_("Feedback turi"),
    )
    body = models.TextField(
        validators=[MaxLengthValidator(1000)], verbose_name=_("Mazmuni")
    )

    answered = models.BooleanField(
        default=False, verbose_name=_("Javob berildimi")
    )

    user = models.ForeignKey(
        "http.User",
        on_delete=models.CASCADE,
        related_name="feedbacks",
        verbose_name=_("Foydalanuvchi"),
    )

    def __str__(self) -> str:
        return f"{self.user} | {self.feedback_type}"

    class Meta:
        db_table = "feedback"
        verbose_name = _("Fikr-mulohaza")
        verbose_name_plural = _("Fikr-mulohazalar")


class Answer(AbstractBaseModel):
    feedback = models.ForeignKey(
        Feedback,
        on_delete=models.CASCADE,
        related_name="answers",
        verbose_name=_("Fikr-mulohaza"),
    )
    body = models.TextField(
        validators=[MaxLengthValidator(1000)], verbose_name=_("Javob")
    )

    def __str__(self) -> str:
        return f"{self.feedback.user} | {self.feedback}"

    class Meta:
        db_table = "answer"
        verbose_name = _("Javob")
        verbose_name_plural = _("Javoblar")
