import os
import csv
from django.conf import settings
from django.core.management import base

from core.http.models import District, Region


class Command(base.BaseCommand):
    help = "Import district data from CSV"

    def handle(self, *args, **options):
        csv_path = os.path.join(settings.BASE_DIR, 'assets/districts.csv')
        if not os.path.exists(csv_path):
            self.stdout.write(self.style.ERROR(f"CSV file not found at {csv_path}"))
            return

        try:
            with open(csv_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    try:
                        region = Region.objects.get(id=int(row["region_id"]))
                        District.objects.create(
                            region=region,
                            district_uz=row['name_uz'],
                            district_ru=row['name_oz'],
                            district_en=row['name_ru']
                        )
                        self.stdout.write(self.style.SUCCESS(f"District {row['name_uz']} added"))
                    except Region.DoesNotExist:
                        self.stdout.write(self.style.ERROR(f"Region with id {row['region_id']} does not exist"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {e}"))
