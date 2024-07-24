from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin

from core.apps.classcom.models import Notification


@admin.register(Notification)
class NotificationAdmin(TabbedTranslationAdmin):
    list_display = ("id", "user", "message", "is_read", "created_at")
    search_fields = ("user", "message")
