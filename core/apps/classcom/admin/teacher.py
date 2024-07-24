from django.contrib import admin

from core.apps.classcom.models import Teacher


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "payment_status",
    )
