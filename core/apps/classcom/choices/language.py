from django.db import models
from django.utils.translation import gettext_lazy as _


class Language(models.TextChoices):
    uz = "uz", _("O'zbek tili")
    ru = "ru", _("Rus tili")


class LanguageModel(models.Model):
    language = models.CharField(
        max_length=2,
        choices=Language.choices,
        verbose_name=_("Til"),
    )
    name = models.CharField(
        max_length=255,
        verbose_name=_("Nomi"),
    )

    def __str__(self):
        return self.language

    def save(self, *args, **kwargs):
        if self.language == Language.uz:
            self.name = "O'zbek tili"
            self.name_ru = "Узбекский язык"
            self.name_uz = "O'zbek tili"
        elif self.language == Language.ru:
            self.name = "Rus tili"
            self.name_ru = "Русский язык"
            self.name_uz = "Rus tili"
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("Til")
        verbose_name_plural = _("Tillar")
