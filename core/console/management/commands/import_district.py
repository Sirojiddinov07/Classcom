import csv
import os

from django.conf import settings
from django.core.management import base

from core.http.models import Region, District


class Command(base.BaseCommand):
    help = "Import district data from CSV"

    def handle(self, *args, **options):
        csv_path = os.path.join(settings.BASE_DIR, "assets/districts.csv")
        if not os.path.exists(csv_path):
            self.stdout.write(
                self.style.ERROR(f"CSV file not found at {csv_path}")
            )
            return

        try:
            with open(csv_path, newline="", encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    id = row.get("id")
                    region_id = row.get("region_id")
                    district_uz = row.get("name_uz")
                    district_ru = row.get("name_ru")
                    district_en = row.get("name_oz")

                    if not region_id or not district_uz:
                        self.stdout.write(
                            self.style.ERROR(
                                f"Skipping row with missing data: {row}"
                            )
                        )
                        continue

                    try:
                        region = Region.objects.filter(
                            id=int(region_id)
                        ).first()
                        if not region:
                            self.stdout.write(
                                self.style.ERROR(
                                    f"Region with id {region_id} does not exist"
                                )
                            )
                            continue

                        # Try to find an existing district by region and district_uz
                        district = District.objects.filter(
                            region=region, district_uz=district_uz
                        ).first()
                        if not district:
                            # If not found by district_uz, try finding by district_ru
                            if district_ru:
                                district = District.objects.filter(
                                    region=region, district_ru=district_ru
                                ).first()
                            # If still not found, try finding by district_en
                            if not district and district_en:
                                district = District.objects.filter(
                                    region=region, district_en=district_en
                                ).first()

                        if district:
                            if id:
                                district.id = id
                            if (
                                district_ru
                                and district.district_ru != district_ru
                            ):
                                district.district_ru = district_ru
                            if (
                                district_en
                                and district.district_en != district_en
                            ):
                                district.district_en = district_en
                            if (
                                district_uz
                                and district.district_uz != district_uz
                            ):
                                district.district_uz = district_uz
                            district.save()
                            self.stdout.write(
                                self.style.SUCCESS(
                                    f"District {district_uz} updated"
                                )
                            )
                        else:
                            District.objects.update_or_create(
                                id=id,
                                defaults={
                                    "region": region,
                                    "district_uz": district_uz,
                                    "district_ru": district_ru,
                                    "district_en": district_en,
                                },
                            )
                            self.stdout.write(
                                self.style.SUCCESS(
                                    f"District {district_uz} added"
                                )
                            )

                    except Exception as e:
                        self.stdout.write(
                            self.style.ERROR(
                                f"Error while processing row {row}: {e}"
                            )
                        )

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {e}"))
