from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin

from core.apps.classcom.models import Notification
from django.utils.translation import gettext_lazy as _


@admin.register(Notification)
class NotificationAdmin(TabbedTranslationAdmin):
    list_display = ("id", "full_name", "message", "is_read", "created_at")
    search_fields = (
        "user__first_name",
        "message",
        "user__last_name",
        "user__phone",
    )

    def full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

    full_name.short_description = _("Ism Familiya")
