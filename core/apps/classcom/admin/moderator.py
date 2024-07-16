from django.contrib import admin
from core.apps.classcom.models import Moderator


@admin.register(Moderator)
class ModeratorAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "is_contracted",
    )
    search_fields = ("user",)
    autocomplete_fields = ("user",)
