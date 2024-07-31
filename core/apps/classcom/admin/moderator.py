from django.contrib import admin

from core.apps.classcom.models import Moderator,  TempModerator


@admin.register(Moderator)
class ModeratorAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "is_contracted",
    )
    search_fields = ("user",)


@admin.register(TempModerator)
class TempModeratorAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "is_contracted",
    )
    search_fields = ("user",)
