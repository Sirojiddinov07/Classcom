from django.core.validators import MaxLengthValidator
from django.db import models

from core.http.choices.feedback import FeedbackType
from core.http.models.base import AbstractBaseModel


class Feedback(AbstractBaseModel):
    feedback_type = models.CharField(
        max_length=10, choices=FeedbackType.choices
    )
    body = models.TextField(validators=[MaxLengthValidator(1000)])

    answered = models.BooleanField(default=False)

    user = models.ForeignKey(
        "http.User", on_delete=models.CASCADE, related_name="feedbacks"
    )

    def __str__(self) -> str:
        return f"{self.user} | {self.feedback_type}"

    class Meta:
        db_table = "feedback"
        verbose_name = "Feedback"
        verbose_name_plural = "Feedbacks"


class Answer(AbstractBaseModel):
    feedback = models.ForeignKey(
        Feedback, on_delete=models.CASCADE, related_name="answers"
    )
    body = models.TextField(validators=[MaxLengthValidator(1000)])

    def __str__(self) -> str:
        return f"{self.feedback.user} | {self.feedback}"

    class Meta:
        db_table = "naswer"
        verbose_name = "Answer"
        verbose_name_plural = "Answers"
