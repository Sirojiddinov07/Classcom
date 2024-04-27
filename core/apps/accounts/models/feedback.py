from django.core.validators import MaxLengthValidator
from django.db import models
from core.http.models.base import AbstractBaseModel

from core.http.models.user import User


class Feedback(AbstractBaseModel):
    class FeedbackType(models.TextChoices):
        firsttype = "first" # TODO o'zgaruvchi nomi o'zgartirilish
        second = "second" # TODO o'zgaruvchi nomi o'zgartirilishi
    feedback_type = models.CharField(max_length=10, choices=FeedbackType.choices)
    body = models.TextField(validators=[MaxLengthValidator(1000)])

    answered = models.BooleanField(default=False)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedbacks')

    def __str__(self) -> str:
        return f"{self.user} | {self.feedback_type}"
    
    class Meta:
        db_table = 'feedback'
        verbose_name = 'Feedback'
        verbose_name_plural = 'Feedbacks'


class Answer(AbstractBaseModel):
    body = models.TextField(validators=[MaxLengthValidator(1000)])
    feedback = models.ForeignKey(Feedback, on_delete=models.CASCADE, related_name='answers')

    def __str__(self) -> str:
        return f"{self.user} | {self.feedback}"
    
    class Meta:
        db_table = 'naswer'
        verbose_name = 'Answer'
        verbose_name_plural = 'Answers'
