import math
from datetime import datetime, timedelta

from django.contrib.auth import models as auth_models
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.apps.classcom.choices import Role
from core.apps.classcom.models import Science, Classes
from core.http import choices, managers
from core.http.models import AbstractBaseModel


class User(auth_models.AbstractUser, AbstractBaseModel):
    phone = models.CharField(
        max_length=255, unique=True, verbose_name=_("Telefon")
    )
    username = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Foydalanuvchi nomi"),
    )
    avatar = models.ImageField(
        upload_to="avatar/", blank=True, null=True, verbose_name=_("Avatar")
    )
    validated_at = models.DateTimeField(
        null=True, blank=True, verbose_name=_("Tasdiqlangan vaqti")
    )
    role = models.CharField(
        max_length=255,
        choices=Role,
        default=Role.USER,
        verbose_name=_("Rol"),
    )

    region = models.ForeignKey(
        "Region",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Viloyat"),
    )
    district = models.ForeignKey(
        "District",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Tuman"),
    )
    institution = models.CharField(
        max_length=255,
        choices=choices.Institution.choices,
        null=True,
        blank=True,
        verbose_name=_("Muassasa"),
    )
    science_group = models.ForeignKey(
        "ScienceGroups",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Fan guruhi"),
    )
    school_type = models.ForeignKey(
        "SchoolType",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Maktab turi"),
    )
    institution_number = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Muassasa raqami"),
    )
    classes = models.ForeignKey(
        Classes,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Sinflar"),
    )
    science = models.ForeignKey(
        Science,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Fan"),
    )

    USERNAME_FIELD = "phone"

    objects = managers.UserManager()

    def __str__(self) -> str:
        return str(self.phone)

    def save(self, *args, **kwargs):
        self.username = self.phone
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("Foydalanuvchilar")
        verbose_name_plural = _("Foydalanuvchilar")
        ordering = ["-created_at"]


class SmsConfirm(AbstractBaseModel):
    SMS_EXPIRY_SECONDS = 120
    RESEND_BLOCK_MINUTES = 10
    TRY_BLOCK_MINUTES = 2
    RESEND_COUNT = 5
    TRY_COUNT = 10

    code = models.IntegerField(verbose_name=_("Kod"))
    try_count = models.IntegerField(
        default=0, verbose_name=_("Urinishlar soni")
    )
    resend_count = models.IntegerField(
        default=0, verbose_name=_("Qayta yuborishlar soni")
    )
    phone = models.CharField(max_length=255, verbose_name=_("Telefon raqami"))
    expire_time = models.DateTimeField(
        null=True, blank=True, verbose_name=_("Muddati")
    )
    unlock_time = models.DateTimeField(
        null=True, blank=True, verbose_name=_("Bloklanish vaqti")
    )
    resend_unlock_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Qayta yuborish bloklanish vaqti"),
    )

    def sync_limits(self):
        if self.resend_count >= self.RESEND_COUNT:
            self.try_count = 0
            self.resend_count = 0
            self.resend_unlock_time = datetime.now() + timedelta(
                minutes=self.RESEND_BLOCK_MINUTES
            )
        elif self.try_count >= self.TRY_COUNT:
            self.try_count = 0
            self.unlock_time = datetime.now() + timedelta(
                minutes=self.TRY_BLOCK_MINUTES
            )

        if (
            self.resend_unlock_time is not None
            and self.resend_unlock_time.timestamp()
            < datetime.now().timestamp()
        ):
            self.resend_unlock_time = None

        if (
            self.unlock_time is not None
            and self.unlock_time.timestamp() < datetime.now().timestamp()
        ):
            self.unlock_time = None
        self.save()

    def is_expired(self):
        return (
            self.expire_time.timestamp() < datetime.now().timestamp()
            if hasattr(self.expire_time, "timestamp")
            else None
        )

    def is_block(self):
        return self.unlock_time is not None

    def reset_limits(self):
        self.try_count = 0
        self.resend_count = 0
        self.unlock_time = None

    def interval(self, time):
        expire = time.timestamp() - datetime.now().timestamp()
        minutes = math.floor(expire / 60)
        expire -= minutes * 60
        expire = math.floor(expire)

        return f"{minutes:02d}:{expire:02d}"

    def __str__(self) -> str:
        return f"{self.phone} | {self.code}"
