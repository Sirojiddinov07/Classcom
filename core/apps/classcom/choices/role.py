from django.db import models
from django.utils.translation import gettext_lazy as __


class Role(models.TextChoices):
    ADMIN = 'admin', __("Administrator")
    MODERATOR = 'moderator', __("Moderator")
    USER = 'user', __("User")
