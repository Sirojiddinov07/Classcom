from django.contrib import admin
from core.apps.classcom import models

admin.site.register(models.Resource)
admin.site.register(models.Topic)
admin.site.register(models.Classes)
admin.site.register(models.Quarter)
admin.site.register(models.Science)
admin.site.register(models.Media)
