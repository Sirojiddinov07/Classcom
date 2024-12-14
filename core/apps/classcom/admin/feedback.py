from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin, TabularInline

from core.apps.classcom.models import Answer, Feedback


class InlineAnswer(TabularInline):
    model = Answer
    fields = ["body"]
    extra = 0


@admin.register(Feedback)
class FeedbackAdmin(ModelAdmin):
    inlines = [InlineAnswer]
    list_display = ("id", "full_name", "feedback_type", "answered")
    autocomplete_fields = ("user",)

    def full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

    full_name.short_description = _("Ism Familiya")


@admin.register(Answer)
class AnswerAdmin(ModelAdmin):
    list_display = ("id", "feedback", "body")
    search_fields = ("feedback", "body")
    list_filter = ("feedback",)
    autocomplete_fields = ("feedback",)
