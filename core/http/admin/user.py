from django.contrib.admin import StackedInline
from django.contrib.auth import admin
from import_export import admin as import_export

from core.apps.classcom.choices import Role
from core.apps.classcom.models import Moderator
from core.http.forms import CustomUserCreationForm


# class CustomUserAdmin(admin.UserAdmin, import_export.ImportExportModelAdmin):
#     list_display = (
#         "first_name",
#         "last_name",
#         "phone",
#     )


class GroupAdmin(import_export.ImportExportModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]

    filter_horizontal = ("permissions",)


class ModeratorInline(StackedInline):
    model = Moderator
    can_delete = False
    verbose_name_plural = "Moderators"
    fields = [
        "balance",
        "degree",
        "docs",
        "is_contracted",
    ]


class UserAdmin(admin.UserAdmin, import_export.ImportExportModelAdmin):
    add_form = CustomUserCreationForm
    list_display = ["phone", "first_name", "last_name", "role"]
    search_fields = ["phone", "first_name", "last_name"]
    list_filter = ["role"]
    fieldsets = (
        (None, {"fields": ("username", "phone", "password")}),
        (
            "Personal info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "role",
                    "region",
                    "district",
                    "avatar",
                    "science",
                    "institution",
                    "science_group",
                    "institution_number",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    def get_inlines(self, request, obj=None):
        inlines = list(super().get_inlines(request, obj))
        if obj and obj.role == Role.MODERATOR:
            inlines.append(ModeratorInline)
        return inlines

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("phone", "password1", "password2"),
            },
        ),
    )
