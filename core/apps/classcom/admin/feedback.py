from django.contrib import admin

from ..models.feedback import *


class InlineAnswer(admin.TabularInline):
    model = Answer
    fields = ["body"]
    extra = 1


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    inlines = [InlineAnswer]
    list_display = ("user", "id", "feedback_type", "answered")


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ("id", "feedback", "body")
    search_fields = ("feedback", "body")
    list_filter = ("feedback",)
