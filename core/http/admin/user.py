from django.contrib.auth import admin
from import_export import admin as import_export
from unfold.admin import ModelAdmin, StackedInline

# from core.http.forms import CustomUserCreationForm
from unfold.forms import (
    AdminPasswordChangeForm,
    UserChangeForm,
    UserCreationForm,
)

from core.apps.classcom.choices import Role
from core.apps.classcom.models import Moderator


# class CustomUserAdmin(admin.UserAdmin, import_export.ImportExportModelAdmin):
#     list_display = (
#         "first_name",
#         "last_name",
#         "phone",
#     )


class GroupAdmin(ModelAdmin, import_export.ImportExportModelAdmin):
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
    readonly_fields = ["balance"]


class UserAdmin(
    admin.UserAdmin, ModelAdmin, import_export.ImportExportModelAdmin
):
    change_password_form = AdminPasswordChangeForm
    add_form = UserCreationForm
    form = UserChangeForm
    list_filter_submit = True
    list_display = ["id", "phone", "first_name", "last_name", "role"]
    search_fields = ["phone", "first_name", "last_name"]
    list_filter = ["role"]
    fieldsets = (
        (
            "User",
            {"classes": ["tab"], "fields": ("username", "phone", "password")},
        ),
        (
            "Personal info",
            {
                "classes": ["tab"],
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
                    "school_type",
                    "class_group",
                ),
            },
        ),
        (
            "Permissions",
            {
                "classes": ["tab"],
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (
            "Important dates",
            {"classes": ["tab"], "fields": ("last_login", "date_joined")},
        ),
    )

    def get_inlines(self, request, obj=None):
        inlines = list(super().get_inlines(request, obj))
        if obj and obj.role == Role.MODERATOR or obj.role == Role.USER:
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
