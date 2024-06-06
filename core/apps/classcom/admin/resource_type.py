from django.contrib import admin
from core.apps.classcom import models


@admin.register(models.ResourceType)
class ResourceTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
