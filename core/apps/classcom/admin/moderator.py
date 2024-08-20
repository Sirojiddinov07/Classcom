from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from core.apps.classcom.models import Moderator, TempModerator


@admin.register(Moderator)
class ModeratorAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "full_name",
        "is_contracted",
        "science",
        "science_group",
    )
    search_fields = ("user__first_name", "user__last_name", "user__phone")

    def full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

    full_name.short_description = _("Fan o'qituvchisi")

    def science(self, obj):
        return obj.user.science

    science.short_description = _("Fan")

    def science_group(self, obj):
        return obj.user.science_group

    science_group.short_description = _("Fan guruhi")


@admin.register(TempModerator)
class TempModeratorAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "full_name",
        "is_contracted",
        "science",
        "science_group",
    )
    search_fields = ("user",)

    def full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

    full_name.short_description = _("Ism Familiya")

    def science(self, obj):
        return obj.user.science

    science.short_description = _("Fan")

    def science_group(self, obj):
        return obj.user.science_group

    science_group.short_description = _("Fan guruhi")
