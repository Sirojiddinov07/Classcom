from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


def user_has_group_or_permission(user, permission):
    if user.is_superuser:
        return True

    group_names = user.groups.values_list("name", flat=True)
    if not group_names:
        return True

    return user.groups.filter(permissions__codename=permission).exists()


PAGES = [
    {
        "seperator": False,
        "items": [
            {
                "title": _("Bosh sahifa"),
                "icon": "home",
                "link": reverse_lazy("admin:index"),
            },
            {
                "title": _("Statistika"),
                "icon": "monitoring",
                "link": reverse_lazy("dashboard"),
                "permission": lambda request: request.user.is_authenticated,
            },
        ],
    },
    {
        "title": _("Foydalanuvchilar"),
        "separator": True,  # Top border
        "items": [
            {
                "title": _("Foydalanuvchilar"),
                "icon": "person",
                "link": reverse_lazy("admin:http_user_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_user"
                ),
                "badge": lambda: __import__(
                    "core.http.models"
                ).http.models.User.user_get_status_count(),
            },
            {
                "title": _("Guruhlar"),
                "icon": "supervisor_account",
                "link": reverse_lazy("admin:auth_group_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_group"
                ),
            },
            {
                "title": _("Moderatorlar"),
                "icon": "admin_panel_settings",
                "link": reverse_lazy("admin:classcom_moderator_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_moderator"
                ),
                "badge": lambda: __import__(
                    "core.apps.classcom.models"
                ).apps.classcom.models.Moderator.moderator_get_status_count(),
            },
            {
                "title": _("O'qituvchilar"),
                "icon": "school",
                "link": reverse_lazy("admin:classcom_teacher_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_teacher"
                ),
            },
            {
                "title": _("Moderatorni arizasi"),
                "icon": "task_alt",
                "link": reverse_lazy(
                    "admin:classcom_changemoderator_changelist"
                ),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_changemoderator"
                ),
                "badge": lambda: __import__(
                    "core.apps.classcom.models"
                ).apps.classcom.models.ChangeModerator.get_pending(),
            },
        ],
    },
    {
        "title": _("Kalendar Tematik Reja"),
        "separator": True,  # Top border
        "items": [
            {
                "title": _("Tematik reja"),
                "icon": "fact_check",
                "link": reverse_lazy("admin:classcom_plan_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_plan"
                ),
            },
            {
                "title": _("Mavzular"),
                "icon": "checklist",
                "link": reverse_lazy("admin:classcom_topic_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_topic"
                ),
            },
            {
                "title": _("Suniy Intellekt"),
                "icon": "network_intelligence_update",
                "link": reverse_lazy("admin:classcom_ai_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_ai"
                ),
            },
            {
                "title": _("TMR arizalari"),
                "icon": "handshake",
                "link": reverse_lazy("admin:classcom_planappeal_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_planappeal"
                ),
            },
        ],
    },
    {
        "title": _("Elektron resurslar"),
        "separator": True,  # Top border
        "items": [
            {
                "title": _("Elektron resurslar"),
                "icon": "picture_as_pdf",
                "link": reverse_lazy("admin:classcom_resource_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_resource"
                ),
            },
            {
                "title": _("Resurs turlari"),
                "icon": "border_color",
                "link": reverse_lazy("admin:classcom_resourcetype_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_resourcetype"
                ),
            },
            {
                "title": _("Kategoriyalar"),
                "icon": "format_list_numbered",
                "link": reverse_lazy("admin:classcom_category_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_category"
                ),
            },
            {
                "title": _("Kategoriya turlari"),
                "icon": "format_indent_increase",
                "link": reverse_lazy("admin:classcom_categorytype_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_categorytype"
                ),
            },
        ],
    },
    {
        "title": _("Maktablar"),
        "separator": True,  # Top border
        "items": [
            {
                "title": _("Maktab turi"),
                "icon": "history_edu",
                "link": reverse_lazy("admin:http_schooltype_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_schooltype"
                ),
            },
        ],
    },
    {
        "title": _("Sinflar"),
        "separator": True,  # Top border
        "items": [
            {
                "title": _("Sinflar"),
                "icon": "class",
                "link": reverse_lazy("admin:classcom_classes_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_classes"
                ),
            },
            {
                "title": _("Sinf Guruhi"),
                "icon": "ad_group",
                "link": reverse_lazy("admin:classcom_classtype_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_classtype"
                ),
            },
            {
                "title": _("Sinf turi"),
                "icon": "border_color",
                "link": reverse_lazy("admin:http_classgroup_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_classgroup"
                ),
            },
        ],
    },
    {
        "title": _("Dars jadvali"),
        "separator": True,  # Top border
        "items": [
            {
                "title": _("Darslar"),
                "icon": "pending_actions",
                "link": reverse_lazy("admin:classcom_schedule_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_schedule"
                ),
            },
            {
                "title": _("Dars jadval shablonlari"),
                "icon": "tab_recent",
                "link": reverse_lazy(
                    "admin:classcom_scheduletemplate_changelist"
                ),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_scheduletemplate"
                ),
            },
            {
                "title": _("Dars jadvali tanlash"),
                "icon": "event_available",
                "link": reverse_lazy(
                    "admin:classcom_schedulechoices_changelist"
                ),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_schedulechoices"
                ),
            },
            {
                "title": _("Dam olish kunlari"),
                "icon": "free_cancellation",
                "link": reverse_lazy("admin:classcom_daysoff_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_daysoff"
                ),
            },
            {
                "title": _("Choraklar"),
                "icon": "dashboard_customize",
                "link": reverse_lazy("admin:classcom_quarter_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_quarter"
                ),
            },
            {
                "title": _("Haftalar"),
                "icon": "date_range",
                "link": reverse_lazy("admin:classcom_weeks_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_weeks"
                ),
            },
        ],
    },
    {
        "title": _("Qo'llab quvvatlash"),
        "separator": True,  # Top border
        "items": [
            {
                "title": _("Bildirishnomalar"),
                "icon": "notifications",
                "link": reverse_lazy(
                    "admin:websocket_notification_changelist"
                ),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_notification"
                ),
            },
            {
                "title": _("Chat"),
                "icon": "forum",
                "link": reverse_lazy("admin:classcom_chat_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_chat"
                ),
            },
            {
                "title": _("Fikr mulohazalar"),
                "icon": "share_reviews",
                "link": reverse_lazy("admin:classcom_feedback_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_feedback"
                ),
            },
            {
                "title": _("Javoblar"),
                "icon": "mark_chat_read",
                "link": reverse_lazy("admin:classcom_answer_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_answer"
                ),
            },
        ],
    },
    {
        "title": _("Fanlar"),
        "separator": True,  # Top border
        "items": [
            {
                "title": _("Fanlar"),
                "icon": "psychology",
                "link": reverse_lazy("admin:classcom_science_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_science"
                ),
            },
            {
                "title": _("Fan turlari"),
                "icon": "experiment",
                "link": reverse_lazy("admin:classcom_sciencetypes_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_sciencetypes"
                ),
            },
            {
                "title": _("Fan guruhi"),
                "icon": "psychology_alt",
                "link": reverse_lazy("admin:http_sciencegroups_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_sciencegroups"
                ),
            },
        ],
    },
    {
        "title": _("Manzillar"),
        "separator": True,  # Top border
        "items": [
            {
                "title": _("Viloyatlar"),
                "icon": "location_on",
                "link": reverse_lazy("admin:http_region_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_region"
                ),
            },
            {
                "title": _("Tumanlar"),
                "icon": "my_location",
                "link": reverse_lazy("admin:http_district_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_district"
                ),
            },
        ],
    },
    {
        "title": _("Fayllar"),
        "separator": True,  # Top border
        "items": [
            {
                "title": _("Media Fayllar"),
                "icon": "share",
                "link": reverse_lazy("admin:classcom_media_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_media"
                ),
            },
            {
                "title": _("Hujjatlar"),
                "icon": "folder_open",
                "link": reverse_lazy("admin:classcom_document_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_document"
                ),
            },
            {
                "title": _("TMR Fayllari"),
                "icon": "drive_folder_upload",
                "link": reverse_lazy("admin:classcom_tmrfiles_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_tmrfiles"
                ),
            },
            {
                "title": _("Yuklashlar"),
                "icon": "download",
                "link": reverse_lazy("admin:classcom_download_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_download"
                ),
            },
        ],
    },
    {
        "title": _("To'lovlar"),
        "separator": True,  # Top border
        "items": [
            {
                "title": _("Buyurtmalar"),
                "icon": "shopping_cart",
                "link": reverse_lazy("admin:payments_orders_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_orders"
                ),
            },
            {
                "title": _("To'lovlar"),
                "icon": "attach_money",
                "link": reverse_lazy("admin:payments_payments_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_payments"
                ),
            },
            {
                "title": _("Tariflar"),
                "icon": "shopping_bag",
                "link": reverse_lazy("admin:payments_plans_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_plans"
                ),
            },
        ],
    },
    {
        "title": _("Qo'shimcha"),
        "separator": True,  # Top border
        "items": [
            {
                "title": _("Sozlamalar"),
                "icon": "settings",
                "link": reverse_lazy("admin:classcom_settings_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_settings"
                ),
            },
            {
                "title": _("Tillar"),
                "icon": "translate",
                "link": reverse_lazy(
                    "admin:classcom_languagemodel_changelist"
                ),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_languagemodel"
                ),
            },
            {
                "title": _("SMS tasdiqlash"),
                "icon": "feedback",
                "link": reverse_lazy("admin:http_smsconfirm_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_smsconfirm"
                ),
            },
        ],
    },
]
