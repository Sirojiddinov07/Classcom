from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin
from unfold.admin import ModelAdmin

from core.apps.classcom.models import Classes, ClassType


@admin.register(Classes)
class ClassesAdmin(ModelAdmin, TabbedTranslationAdmin):
    list_display = ("id", "name", "type")
    search_fields = ("name",)


@admin.register(ClassType)
class ClassTypeAdmin(ModelAdmin, TabbedTranslationAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
