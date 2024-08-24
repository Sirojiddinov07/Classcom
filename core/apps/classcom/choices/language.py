from django.db import models
from django.utils.translation import gettext_lazy as _


class Language(models.TextChoices):
    uz = "uz", _("O'zbek tili")
    ru = "ru", _("Rus tili")


class LanguageModel(models.Model):
    language = models.CharField(
        max_length=2,
        choices=Language.choices,
    )
