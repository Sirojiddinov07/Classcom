from django.contrib.admin import site
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views import View

from core.apps.classcom.models import Resource, Feedback, Plan
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
                    "title": _("Fikrlar"),
                    "value": self.feedback.all().count(),
                },
                {
                    "title": _("Javob berilgan fikrlar"),
                    "value": self.feedback.filter(answered=True).count(),
                },
                {
                    "title": _("Javob berilmagan fikrlar"),
                    "value": self.feedback.filter(answered=False).count(),
                },
            ]
            # Cache the result for 5 minutes
            cache.set("dashboard_cards", cards, 300)
        return cards

    def get(self, request):
        context = dict(site.each_context(request))

        # ! Context
        context.update({"cards": self.get_cards()})

        return render(request, "admin/dashboard.html", context)
