from django.contrib import admin
from django.db import models as db_model
from django_select2 import forms as django_select2
from import_export.admin import ImportExportModelAdmin
from modeltranslation.admin import TabbedTranslationAdmin
from unfold.admin import ModelAdmin

from core.http import forms, models


class PostInline(admin.TabularInline):
    model = models.Post.comments.through
    fields = ["comment"]
    extra = 1


class TagsInline(admin.TabularInline):
    model = models.Post.tags.through
    extra = 1


class PostAdmin(
    ModelAdmin,
    TabbedTranslationAdmin,
    ImportExportModelAdmin,
):  # noqa
    fields: tuple = ("title", "desc", "image", "tags")
    search_fields: list = ["title", "desc"]
    list_filter = ["title"]
    required_languages: tuple = ("uz",)
    form = forms.PostAdminForm
    inlines = [PostInline]
    formfield_overrides = {
        db_model.ManyToManyField: {
            "widget": django_select2.Select2MultipleWidget
        }
    }


class TagsAdmin(ModelAdmin, ImportExportModelAdmin):
    fields: tuple = ("name",)
    search_fields: list = ["name"]


class FrontendTranslationAdmin(ModelAdmin, ImportExportModelAdmin):  # noqa
    fields: tuple = ("key", "value")
    required_languages: tuple = ("uz",)
    list_display = ["key", "value"]


class SmsConfirmAdmin(ModelAdmin):
    list_display = ["id", "phone", "code", "resend_count", "try_count"]
    search_fields = ["phone", "code"]
    ordering = ["-created_at"]


class CommentAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ["text"]
    search_fields = ["text"]
