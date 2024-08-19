from django.db import models
from django.utils.translation import gettext_lazy as _


class Weekday(models.TextChoices):
    monday = "monday", _("Dushanba")
    tuesday = "tuesday", _("Seshanba")
    wednesday = "wednesday", _("Chorshanba")
    thursday = "thursday", _("Payshanba")
    friday = "friday", _("Juma")
    saturday = "saturday", _("Shanba")
