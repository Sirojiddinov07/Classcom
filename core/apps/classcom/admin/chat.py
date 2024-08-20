from django.contrib import admin

from core.apps.classcom.models import Chat
from django.utils.translation import gettext_lazy as _


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "full_name",
        "massage",
        "time",
        "response",
        "response_time",
    )
    exclude = ("response_time",)
    search_fields = ("user__first_name", "user__last_name", "user__phone")

    def full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

    full_name.short_description = _("Ism Familiya")
