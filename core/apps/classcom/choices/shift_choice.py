from django.db import models
from django.utils.translation import gettext_lazy as __


class ShiftChoice(models.TextChoices):
    MORNING = "MORNING", __("morning")
    EVENING = "EVENING", __("evening")
