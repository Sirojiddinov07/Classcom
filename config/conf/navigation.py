from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

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
            },
            {
                "title": _("Guruhlar"),
                "icon": "supervisor_account",
                "link": reverse_lazy("admin:auth_group_changelist"),
            },
            {
                "title": _("Moderatorlar"),
                "icon": "admin_panel_settings",
                "link": reverse_lazy("admin:classcom_moderator_changelist"),
            },
            {
                "title": _("O'qituvchilar"),
                "icon": "school",
                "link": reverse_lazy("admin:classcom_teacher_changelist"),
            },
            {
                "title": _("Temp Moderators"),
                "icon": "remove_moderator",
                "link": reverse_lazy(
                    "admin:classcom_tempmoderator_changelist"
                ),
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
            },
            {
                "title": _("Mavzular"),
                "icon": "checklist",
                "link": reverse_lazy("admin:classcom_topic_changelist"),
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
            },
            {
                "title": _("Resurs turlari"),
                "icon": "border_color",
                "link": reverse_lazy("admin:classcom_resourcetype_changelist"),
            },
            {
                "title": _("Kategoriyalar"),
                "icon": "format_list_numbered",
                "link": reverse_lazy("admin:classcom_category_changelist"),
            },
            {
                "title": _("Kategoriya turlari"),
                "icon": "format_indent_increase",
                "link": reverse_lazy("admin:classcom_categorytype_changelist"),
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
            },
            {
                "title": _("Sinf Guruhi"),
                "icon": "ad_group",
                "link": reverse_lazy("admin:classcom_classtype_changelist"),
            },
            {
                "title": _("Sinf turi"),
                "icon": "border_color",
                "link": reverse_lazy("admin:http_classgroup_changelist"),
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
            },
            {
                "title": _("Dars jadval shablonlari"),
                "icon": "tab_recent",
                "link": reverse_lazy(
                    "admin:classcom_scheduletemplate_changelist"
                ),
            },
            {
                "title": _("Dars jadvali tanlash"),
                "icon": "event_available",
                "link": reverse_lazy(
                    "admin:classcom_schedulechoices_changelist"
                ),
            },
            {
                "title": _("Dam olish kunlari"),
                "icon": "free_cancellation",
                "link": reverse_lazy("admin:classcom_daysoff_changelist"),
            },
            {
                "title": _("Choraklar"),
                "icon": "dashboard_customize",
                "link": reverse_lazy("admin:classcom_quarter_changelist"),
            },
            {
                "title": _("Haftalar"),
                "icon": "date_range",
                "link": reverse_lazy("admin:classcom_weeks_changelist"),
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
            },
            {
                "title": _("Chat"),
                "icon": "forum",
                "link": reverse_lazy("admin:classcom_chat_changelist"),
            },
            {
                "title": _("Fikr mulohazalar"),
                "icon": "share_reviews",
                "link": reverse_lazy("admin:classcom_feedback_changelist"),
            },
            {
                "title": _("Javoblar"),
                "icon": "mark_chat_read",
                "link": reverse_lazy("admin:classcom_answer_changelist"),
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
            },
            {
                "title": _("Fan turlari"),
                "icon": "experiment",
                "link": reverse_lazy("admin:classcom_sciencetypes_changelist"),
            },
            {
                "title": _("Fan guruhi"),
                "icon": "psychology_alt",
                "link": reverse_lazy("admin:http_sciencegroups_changelist"),
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
            },
            {
                "title": _("Tumanlar"),
                "icon": "my_location",
                "link": reverse_lazy("admin:http_district_changelist"),
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
            },
            {
                "title": _("Yuklashlar"),
                "icon": "download",
                "link": reverse_lazy("admin:classcom_download_changelist"),
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
            },
            {
                "title": _("To'lovlar"),
                "icon": "attach_money",
                "link": reverse_lazy("admin:payments_payments_changelist"),
            },
            {
                "title": _("Tariflar"),
                "icon": "shopping_bag",
                "link": reverse_lazy("admin:payments_plans_changelist"),
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
            },
            {
                "title": _("Tillar"),
                "icon": "translate",
                "link": reverse_lazy(
                    "admin:classcom_languagemodel_changelist"
                ),
            },
            {
                "title": _("SMS tasdiqlash"),
                "icon": "feedback",
                "link": reverse_lazy("admin:http_smsconfirm_changelist"),
            },
        ],
    },
]
