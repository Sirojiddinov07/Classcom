from django.db import models
from django.utils.translation import gettext_lazy as __


class Degree(models.TextChoices):
    HIGHER = "HIGHER", __("Oliy toifa")
    EXCELLENT = "EXCELLENT", __("Xalq ta'limi a'lochisi")
    GOOD_TEACHER = "GOOD_TEACHER", __(
        "\"Eng yaxshi o'qituvchi\" konkursi g'olibi"
    )  # noqa
    AUTHOR = "AUTHOR", __("Darslik muallifi")
