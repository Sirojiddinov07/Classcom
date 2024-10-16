from typing import Any

from django.core.exceptions import ObjectDoesNotExist
from django.core.management import BaseCommand

from core.http import models


class Command(BaseCommand):
    help = "Create user"

    def handle(self, *args: Any, **options: Any) -> str | None:
        phone = ["330078587", "998946593659"]
        password = ["20030307mart", "20030307mart"]
        for i in range(len(phone)):
            try:
                models.User.objects.get(phone=phone[i])
            except ObjectDoesNotExist:
                models.User.objects.create_superuser(phone[i], password[i])
