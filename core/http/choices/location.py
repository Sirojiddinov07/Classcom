from django.db import models
from django.utils.translation import gettext_lazy as _


class Institution(models.TextChoices):
    OLIY = "OLIY", _("Oliy")
    OSMAN = "O'rta maxsus", _("O'rta maxsus")
    YOSH = "O'rta", _("O'rta")
