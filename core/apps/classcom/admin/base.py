from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from core.apps.classcom import models
from core.apps.classcom import resources


class PlanAdmin(ImportExportModelAdmin):
    """
    Cosutimize the plan model in admin panel interface
    """

    resource_class = resources.PlanResource


admin.site.register(models.Topic)
admin.site.register(models.Media)
admin.site.register(models.Classes)
admin.site.register(models.Quarter)
admin.site.register(models.Teacher)
admin.site.register(models.Science)
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