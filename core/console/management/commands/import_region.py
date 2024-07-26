import os
import csv
from django.conf import settings
from django.core.management import base

from core.http.models import Region


class Command(base.BaseCommand):
    help = "Import CSV data into Region model"

    def add_arguments(self, parser):
        parser.add_argument("csv_path", nargs='?', default=os.path.join(settings.BASE_DIR, 'assets/regions.csv'))

    def handle(self, *args, **options):
        csv_path = options.get("csv_path")

        if not os.path.exists(csv_path):
            self.stdout.write(self.style.ERROR(f"CSV file not found at {csv_path}"))
            return

        try:
            with open(csv_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    Region.objects.create(
                        region_uz=row['name_uz'],
                        region_ru=row['name_oz'],
                        region_en=row['name_ru']
                    )
                    self.stdout.write(self.style.SUCCESS(f"Region {row['name_uz']} added"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {e}"))
