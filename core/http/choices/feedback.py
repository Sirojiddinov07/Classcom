from django.db import models


class FeedbackType(models.TextChoices):
    first = "first"  # TODO o'zgaruvchi nomini o'zgartirish
    second = "second"  # TODO o'zgaruvchi nomini o'zgartirilish
