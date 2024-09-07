from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin

from core.apps.classcom.models import Moderator, TempModerator


from django.utils.html import format_html


@admin.register(Moderator)
class ModeratorAdmin(ModelAdmin):
    list_display = (
        "id",
        "full_name",
        "is_contracted",
        "degree",
        "docs_links",
    )
    search_fields = ("user__first_name", "user__last_name", "user__phone")
    filter_horizontal = (
        "resource_type",
        "science",
        "science_type",
        "languages",
        "classes",
        "class_groups",
        "quarters",
        "docs",
    )
    ordering = ("-updated_at",)
    fieldsets = (
        (
            None,
            {"fields": ("user", "balance", "degree", "docs", "is_contracted")},
        ),
        (
            _("Plan Permissions"),
            {
                "classes": ["tab"],
                "fields": (
                    "plan_creatable",
                    "languages",
                    "science",
                    "science_type",
                    "classes",
                    "class_groups",
                    "quarters",
                ),
            },
        ),
        (
            _("Resource Permissions"),
            {
                "classes": ["tab"],
                "fields": (
                    "resource_creatable",
                    "resource_type",
                ),
            },
        ),
        (
            _("topic Permissions"),
            {"classes": ["tab"], "fields": ("topic_creatable",)},
        ),
    )

    def full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

    def docs_links(self, obj):
        links = [
            format_html('<a href="{}">{}</a>', doc.url, doc.title)
            for doc in obj.docs.all()
        ]
        return format_html("<br>".join(links))

    docs_links.short_description = _("Hujjatlar")


@admin.register(TempModerator)
class TempModeratorAdmin(ModelAdmin):
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
