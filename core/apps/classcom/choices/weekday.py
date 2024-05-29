from django.db import models
from django.utils.translation import gettext_lazy as _


class Weekday(models.TextChoices):
    dushanba = "dushanba", _("Dushanba")
    seshanba = "seshanba", _("Seshanba")
    chorshanba = "chorshanba", _("Chorshanba")
    payshanba = "payshanba", _("Payshanba")
    juma = "juma", _("Juma")
    shanba = "shanba", _("Shanba")
