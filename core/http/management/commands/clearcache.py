"""
Clear cache command
"""

from typing import Any

from django.core.cache import cache
from django.core.management import BaseCommand

from core.utils import console


class Command(BaseCommand):
    help = "Clear all caches"

    def handle(self, *args: Any, **options: Any) -> None:
        cache.clear()
        console.Console.success(message="Cache cleared successfully")
