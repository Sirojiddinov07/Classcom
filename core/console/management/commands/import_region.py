import os
import csv
from django.conf import settings
from django.core.management import base

from core.http.models import Region


class Command(base.BaseCommand):
    help = "Import CSV data into Region model"

    def add_arguments(self, parser):
        parser.add_argument(
            "csv_path",
            nargs="?",
            default=os.path.join(settings.BASE_DIR, "assets/regions.csv"),
        )

    def handle(self, *args, **options):
        csv_path = options.get("csv_path")

        if not os.path.exists(csv_path):
            self.stdout.write(
                self.style.ERROR(f"CSV file not found at {csv_path}")
            )
            return

        try:
            with open(csv_path, newline="", encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    region_uz = row.get("name_uz", None)
                    region_ru = row.get("name_oz", None)
                    region_en = row.get("name_ru", None)

                    if not region_uz and not region_ru and not region_en:
                        self.stdout.write(
                            self.style.ERROR(
                                f"Skipping row with missing region names: {row}"
                            )
                        )
                        continue

                    region = None
                    try:
                        if region_uz:
                            region = Region.objects.get(region_uz=region_uz)
                        elif region_ru:
                            region = Region.objects.get(region_ru=region_ru)
                        elif region_en:
                            region = Region.objects.get(region_en=region_en)
                    except Region.DoesNotExist:
                        pass
                    except Region.MultipleObjectsReturned:
                        self.stdout.write(
                            self.style.ERROR(
                                f"Multiple regions found for {row}"
                            )
                        )
                        continue

                    if region:
                        if region_uz:
                            region.region_uz = region_uz
                        if region_ru:
                            region.region_ru = region_ru
                        if region_en:
                            region.region_en = region_en
                        region.save()
                        self.stdout.write(
                            self.style.SUCCESS(f"Region updated: {row}")
                        )
                    else:
                        Region.objects.create(
                            region_uz=region_uz,
                            region_ru=region_ru,
                            region_en=region_en,
                        )
                        self.stdout.write(
                            self.style.SUCCESS(f"Region created: {row}")
                        )

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {e}"))
