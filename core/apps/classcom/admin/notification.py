from django.contrib import admin

from core.apps.classcom.models import Notification
from modeltranslation.admin import TabbedTranslationAdmin


@admin.register(Notification)
class NotificationAdmin(TabbedTranslationAdmin):
    list_display = ("id", "user", "message", "is_read", "created_at")
    search_fields = ("user", "message")
