from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin
from unfold.decorators import display

from core.apps.classcom.models import TMRAppeal, TMRAppealStatus, TmrFiles


@admin.register(TMRAppeal)
class TMRAppealAdmin(ModelAdmin):
    list_display = [
        "user",
        "show_status_customized_color",
        "science",
        "science_type",
        "classes",
        "class_groups",
        "docs_links",
    ]
    search_fields = [
        "user__first_name",
        "user__last_name",
        "user__father_name",
    ]
    list_filter = [
        "status",
        "science",
        "science_type",
        "classes",
        "class_groups",
    ]
    readonly_fields = (
        "user",
        "science",
        "science_type",
        "classes",
        "class_groups",
        "created_at",
        "updated_at",
    )

    @display(
        description=_("Status"),
        ordering="status",
        label={
            TMRAppealStatus.ACCEPTED: "success",  # green
            TMRAppealStatus.PENDING: "warning",  # orange
            TMRAppealStatus.REJECTED: "danger",  # red
        },
    )
    def show_status_customized_color(self, obj):
        return obj.status, obj.get_status_display()

    def docs_links(self, obj):
        links = [
            format_html(
                '<a href="{}" target="_blank">{}</a><br>',
                doc.file.url,
                doc.title,
            )
            for doc in TmrFiles.objects.filter(tmr_appeal=obj)
        ]
        return format_html("<br>".join(links))

    docs_links.short_description = _("Fayllar")
