from django.contrib.auth import admin
from import_export import admin as import_export
from core.http.forms import CustomUserCreationForm


class CustomUserAdmin(admin.UserAdmin, import_export.ImportExportModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "phone",
    )


class GroupAdmin(import_export.ImportExportModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]

    filter_horizontal = ("permissions",)


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
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("phone", "password1", "password2"),
            },
        ),
    )
