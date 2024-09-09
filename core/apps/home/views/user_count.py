from django.db.models import Count
from django.shortcuts import render

from core.http.models import Region
from core.http.models.user import User


def user_count_view(request):
    regions = Region.objects.all()

    region_user_counts = User.objects.values("region__region").annotate(
        user_count=Count("id")
    )

    region_user_counts_dict = {
        item["region__region"]: item["user_count"]
        for item in region_user_counts
    }

    region_user_counts = [
        {
            "region__region": region.region,
            "user_count": region_user_counts_dict.get(region.region, 0),
        }
        for region in regions
    ]

    labels = [region["region__region"] for region in region_user_counts]
    data = [region["user_count"] for region in region_user_counts]

    context = {
        "region_user_counts": region_user_counts,
        "labels": labels,
        "data": data,
    }
    print("==============================\n\n")
    print(f"Context: {context}")
    print("==============================\n\n")
    print(f"Data: {data}")
    print("==============================\n\n")
    print(f"Labels: {labels}")
    print("==============================\n\n")

    return render(request, "components/chart.html", context)
