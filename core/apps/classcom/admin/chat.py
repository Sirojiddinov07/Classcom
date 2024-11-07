from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin

from core.apps.classcom.models import Chat


@admin.register(Chat)
class ChatAdmin(ModelAdmin):
    list_display = (
        "id",
        "full_name",
        "massage",
        "time",
        "response",
        "response_time",
        "is_answered",
        "is_read",
    )
    exclude = ("response_time",)
    search_fields = ("user__first_name", "user__last_name", "user__phone")
    list_filter = ("is_answered",)

    def full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

    full_name.short_description = _("Ism Familiya")
