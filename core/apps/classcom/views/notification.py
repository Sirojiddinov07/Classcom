from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View

from core.apps.classcom.forms import NotificationForm
from core.apps.classcom.tasks import create_notification_task


class CreateNotificationFormView(View):
    def get(self, request):
        form = NotificationForm()
        return render(request, "forms/notification.html", {"form": form})

    def post(self, request):
        form = NotificationForm(request.POST)
        if form.is_valid():
            message_uz = form.cleaned_data["message_uz"]
            message_ru = form.cleaned_data["message_ru"]
            user_ids = request.session.get("selected_user_ids", [])
            if not user_ids:
                messages.error(request, "No user IDs found.")
                return redirect(reverse_lazy("admin:http_user_changelist"))
            notifications_created = 0
            for user_id in user_ids:
                try:
                    create_notification_task.delay(
                        user_id=user_id,
                        message_uz=message_uz,
                        message_ru=message_ru,
                    )
                    notifications_created += 1
                except Exception as e:
                    messages.error(
                        request,
                        f"Foydalanuvchi identifikatori uchun bildirishnoma yaratishda xatolik yuz berdi {user_id}: {e}",
                    )
                    return redirect(reverse_lazy("admin:http_user_changelist"))
            messages.success(
                request,
                f"{notifications_created} bildirishnomalar muvaffaqiyatli yaratildi.",
            )
            request.session.pop(
                "selected_user_ids", None
            )  # Clear the session data after use
            return redirect(reverse_lazy("admin:http_user_changelist"))
        else:
            messages.error(request, "Shakl haqiqiy emas.")
            return render(request, "forms/notification.html", {"form": form})
