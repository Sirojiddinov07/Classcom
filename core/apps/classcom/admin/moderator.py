from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin

from core.apps.classcom.models import Moderator


@admin.register(Moderator)
class ModeratorAdmin(ModelAdmin):
    list_display = (
        "id",
        "full_name",
        "is_contracted",
        "degree",
        "docs_links",
        "contract_links",
        "send_contract",
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
    )
    list_filter = (
        "is_contracted",
        "degree",
    )
    ordering = ("-updated_at",)
    readonly_fields = ("docs_links", "balance")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "user",
                    "balance",
                    "degree",
                    "is_contracted",
                    "docs_links",
                )
            },
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
            format_html(
                '<a href="{}" target="_blank">{}</a><br>',
                doc.file.url,
                doc.title,
            )
            for doc in obj.docs.all()
        ]
        return format_html("<br>".join(links))

    docs_links.short_description = _("Hujjatlar")

    def contract_links(self, obj):
        links = [
            format_html(
                '<a href="{}" target="_blank">{}</a><br>',
                doc.file.url,
                doc.title,
            )
            for doc in obj.user.document.all()
        ]
        return format_html("<br>".join(links))

    contract_links.short_description = _("Kelgan shartnoma")

    def send_contract(self, obj):
        links = [
            format_html(
                '<a href="{}" target="_blank">{}</a><br>',
                obj.user.response_file.url,
                _("Shartnoma"),
            )
        ]
        return format_html("<br>".join(links))

    send_contract.short_description = _("Tasdiqlangan shartnoma")
