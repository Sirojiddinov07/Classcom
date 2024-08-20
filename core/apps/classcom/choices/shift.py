from django.db import models
from django.utils.translation import gettext_lazy as _


class ShiftChoice(models.TextChoices):
    MORNING = "MORNING", _("Ertalabki")
    EVENING = "EVENING", _("Kechki")
