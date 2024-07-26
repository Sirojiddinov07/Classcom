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
                    region_id = row.get("region_id")
                    district_uz = row.get('name_uz')
                    district_ru = row.get('name_oz')
                    district_en = row.get('name_ru')

                    if not region_id or not district_uz:
                        self.stdout.write(self.style.ERROR(f"Skipping row with missing data: {row}"))
                        continue

                    try:
                        region = Region.objects.filter(id=int(region_id)).first()
                        if not region:
                            self.stdout.write(self.style.ERROR(f"Region with id {region_id} does not exist"))
                            continue

                        district, created = District.objects.get_or_create(
                            region=region,
                            district_uz=district_uz,
                            defaults={
                                'district_ru': district_ru,
                                'district_en': district_en
                            }
                        )

                        if created:
                            self.stdout.write(self.style.SUCCESS(f"District {district_uz} added"))
                        else:
                            # Update existing district if other names are provided and not already set
                            updated = False
                            if district_ru and district.district_ru != district_ru:
                                district.district_ru = district_ru
                                updated = True
                            if district_en and district.district_en != district_en:
                                district.district_en = district_en
                                updated = True
                            if updated:
                                district.save()
                                self.stdout.write(self.style.SUCCESS(f"District {district_uz} updated"))

                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"Error while processing row {row}: {e}"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {e}"))
