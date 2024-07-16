from django.contrib import admin
from core.apps.classcom.models import Chat


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    exclude = ("response_time",)
