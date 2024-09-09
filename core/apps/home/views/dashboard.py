import json

from django.contrib.admin import site
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.db.models import Count
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views import View

from core.apps.classcom.models import Resource, Feedback, Plan
from core.http.models import Region
from core.http.models import User


@method_decorator(login_required(login_url="/admin/"), name="dispatch")
class DashboardView(View):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.users = User.objects
        self.resource = Resource.objects
        self.feedback = Feedback.objects
        self.plan = Plan.objects

    def get_cards(self):
        # Check cache first
        cards = cache.get("dashboard_cards")
        if not cards:
            cards = [
                {
                    "title": _("Foydalanuvchilar"),
                    "value": self.users.all().count(),
                },
                {
                    "title": _("Moderatorlar"),
                    "value": self.users.filter(role="moderator").count(),
                },
                {
                    "title": _("Ustozlar"),
                    "value": self.users.filter(role="user").count(),
                },
                {
                    "title": _("Elektron resurslar"),
                    "value": self.resource.all().count(),
                },
                {
                    "title": _("Kalendar tematik rejalar"),
                    "value": self.plan.all().count(),
                },
                {
                    "title": _("Barcha sharhlar"),
                    "value": self.feedback.all().count(),
                },
                {
                    "title": _("Javob berilgan sharhlar"),
                    "value": self.feedback.filter(answered=True).count(),
                },
                {
                    "title": _("Javob berilmagan sharhlar"),
                    "value": self.feedback.filter(answered=False).count(),
                },
            ]
            # Cache the result for 5 minutes
            cache.set("dashboard_cards", cards, 300)
        return cards

    def get(self, request):
        context = dict(site.each_context(request))

        # Add cards to context
        context.update({"cards": self.get_cards()})

        # Fetch and process region user counts
        regions = Region.objects.all()
        region_user_counts = User.objects.values("region_id").annotate(
            user_count=Count("id")
        )
        region_user_counts_dict = {
            item["region_id"]: item["user_count"]
            for item in region_user_counts
        }
        region_user_counts = [
            {
                "region_region": region.region,
                "user_count": region_user_counts_dict.get(region.id, 0),
            }
            for region in regions
        ]
        labels = [region["region_region"] for region in region_user_counts]
        data = [region["user_count"] for region in region_user_counts]

        # Update context with region user counts
        context.update(
            {
                "region_user_counts": region_user_counts,
                "labels": json.dumps(labels),
                "data": json.dumps(data),
            }
        )

        return render(request, "admin/dashboard.html", context)
