from django.db import models
from django.utils.translation import gettext_lazy as _


class Weekday(models.TextChoices):
    monday = "monday", _("Monday")
    tuesday = "tuesday", _("Tuesday")
    wednesday = "wednesday", _("Wednesday")
    thursday = "thursday", _("Thursday")
    friday = "friday", _("Friday")
    saturday = "saturday", _("Saturday")
