from django.contrib import admin

from ..models.feedback import *


class InlineAnswer(admin.TabularInline):
    model = Answer
    fields = ['body']
    extra = 1


class FeedbackAdmin(admin.ModelAdmin):
    inlines = [InlineAnswer]
    list_display = ("user", "id", "feedback_type", "answered")

admin.site.register(Answer)
admin.site.register(Feedback, FeedbackAdmin)