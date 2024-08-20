from django.contrib import admin

from core.apps.classcom.models import Answer, Feedback
from django.utils.translation import gettext_lazy as _


class InlineAnswer(admin.TabularInline):
    model = Answer
    fields = ["body"]
    extra = 1


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    inlines = [InlineAnswer]
    list_display = ("id", "full_name", "feedback_type", "answered")

    def full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

    full_name.short_description = _("Ism Familiya")


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ("id", "feedback", "body")
    search_fields = ("feedback", "body")
    list_filter = ("feedback",)
