from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from core.apps.classcom import models
from core.apps.classcom import resources


class PlanAdmin(ImportExportModelAdmin):
    """
    Cosutimize the plan model in admin panel interface
    """

    resource_class = resources.PlanResource


class TopicAdmin(ImportExportModelAdmin):
    """Topic admin

    Args:
        ImportExportModelAdmin (_type_): _description_
    """

    list_display = (
        "name",
        "science",
        "_class",
        "sequence_number",
    )
    search_fields = (
        "name",
        "science__name",
        "_class__name",
    )
    list_filter = (
        "science",
        "_class",
    )
    autocomplete_fields = (
        "science",
        "_class",
    )


class ScienceAdmin(ImportExportModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


class ClassAdmin(ImportExportModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


admin.site.register(models.Topic, TopicAdmin)
admin.site.register(models.Media)
admin.site.register(models.Classes, ClassAdmin)
admin.site.register(models.Quarter)
admin.site.register(models.Teacher)
admin.site.register(models.Science, ScienceAdmin)
admin.site.register(models.Resource)
admin.site.register(models.Schedule)
admin.site.register(models.Settings)
admin.site.register(models.Download)
admin.site.register(models.Moderator)
admin.site.register(models.Plan, PlanAdmin)
admin.site.register(models.DaysOff)


class ChatAdmin(admin.ModelAdmin):
    exclude = ('response_time',)

admin.site.register(models.Chat, ChatAdmin)