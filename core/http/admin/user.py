import logging

from django.contrib import messages
from django.contrib.auth import admin
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from import_export import admin as import_export
from unfold.admin import ModelAdmin
from unfold.admin import StackedInline
from unfold.decorators import action

# from core.http.forms import CustomUserCreationForm
from unfold.forms import (
    AdminPasswordChangeForm,
    UserChangeForm,
    UserCreationForm,
)

from core.apps.classcom.forms import NotificationForm
from core.apps.classcom.models import Moderator
from core.apps.classcom.tasks import create_notification_task
from core.utils import exclude_user

logger = logging.getLogger(__name__)


# class CustomUserAdmin(admin.UserAdmin, import_export.ImportExportModelAdmin):
#     list_display = (
#         "first_name",
#         "last_name",
#         "phone",
#     )


class GroupAdmin(ModelAdmin, import_export.ImportExportModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]

    # filter_horizontal = ("permissions",)
    filter_vertical = ("permissions",)


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
    actions = ["create_notifications_for_users"]
    list_display = ["id", "phone", "first_name", "last_name", "role"]
    search_fields = ["phone", "first_name", "last_name"]
    list_filter = ["role"]
    inlines = [ModeratorInline]
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

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return exclude_user(qs)

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("phone", "password1", "password2"),
            },
        ),
    )

    @action(
        description=_(
            "Tanlangan foydalanuvchilar uchun bildirishnoma yaratish"
        )
    )
    def create_notifications_for_users(self, request: HttpRequest, queryset):
        if request.method == "POST" and request.GET.get("type") == "submit":
            form = NotificationForm(request.POST)
            if form.is_valid():
                message_uz = form.cleaned_data["message_uz"]
                message_ru = form.cleaned_data["message_ru"]
                user_ids = request.session.get("selected_user_ids", [])
                if not user_ids:
                    messages.error(
                        request,
                        "Hech qanday foydalanuvchi identifikatori topilmadi.",
                    )
                    return redirect(reverse_lazy("admin:http_user_changelist"))
                notifications_created = 0
                for user_id in user_ids:
                    try:
                        create_notification_task.delay(
                            user_id=user_id,
                            message_uz=message_uz,
                            message_ru=message_ru,
                        )
                        logger.debug(
                            f"Foydalanuvchi ID uchun bildirishnoma {user_id} created."
                        )
                        notifications_created += 1
                    except Exception as e:
                        logger.error(
                            f"Foydalanuvchi identifikatori uchun bildirishnoma yaratishda xatolik yuz berdi"
                            f" {user_id}: {e}"
                        )
                        messages.error(
                            request,
                            f"Foydalanuvchi identifikatori uchun "
                            f"bildirishnoma yaratishda xatolik yuz berdi "
                            f"{user_id}: {e}",
                        )
                        return redirect(
                            reverse_lazy("admin:http_user_changelist")
                        )
                messages.success(
                    request,
                    f"{notifications_created} bildirishnomalar muvaffaqiyatli yaratildi.",
                )
                request.session.pop(
                    "selected_user_ids", None
                )  # Clear the session data after use
                return redirect(reverse_lazy("admin:http_user_changelist"))
            else:
                messages.error(request, "Forma haqiqiy emas.")
        else:
            user_ids = queryset.values_list("id", flat=True).distinct()
            if user_ids:
                request.session["selected_user_ids"] = list(user_ids)
                return redirect(reverse_lazy("create_notification_form"))
            else:
                messages.error(
                    request,
                    "Hech qanday foydalanuvchi identifikatori topilmadi.",
                )
                return redirect(reverse_lazy("admin:http_user_changelist"))

        return render(
            request,
            "forms/notification.html",
            {"form": form, "queryset": queryset},
        )
