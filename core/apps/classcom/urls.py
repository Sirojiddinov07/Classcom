from django.urls import include, path
from rest_framework import routers

from core.apps.classcom import views
from core.apps.classcom.views import (
    UnifiedSearchView,
    WeeksByQuarterView,
    CreateNotificationFormView,
)
from core.apps.websocket.views import NotificationViewSet
from core.http.views import (
    SchoolTypeViewSet,
    FilteredSchoolGroupViewSet,
    ModeratorClassGroupApiView,
)

router = routers.DefaultRouter()
router.register("feedback", views.FeedbackCreateViewSet, basename="feedback")
router.register("answer", views.AnswerCreateViewSet, basename="answer")
router.register("class", views.ClassesViewSet, basename="class")
router.register("class-type", views.ClassTypeViewSet, basename="class-type")
router.register("science", views.ScienceViewSet, basename="science")
router.register(
    "class-group", FilteredSchoolGroupViewSet, basename="class-group"
)
router.register("schedule", views.ScheduleTemplateViewSet, basename="schedule")
router.register(
    "schedule-choice", views.ScheduleChoiceViewSet, basename="schedule-choice"
)
router.register("days_off", views.DaysOffViewSet, basename="days_off")
router.register("resource", views.ResourceViewSet, basename="resource")
router.register("region", views.RegionViewSet, basename="region")
router.register("district", views.DistrictViewSet, basename="district")
router.register("types", views.ResourceTypesViewSet, basename="types")
router.register(
    "science-types", views.ScienceTypesViewSet, basename="science-types"
)
router.register("school-type", SchoolTypeViewSet, basename="school-type")
router.register("notification", NotificationViewSet, basename="notification")

urlpatterns = [
    path("", include(router.urls)),
    path(
        "create-notification-form/",
        CreateNotificationFormView.as_view(),
        name="create_notification_form",
    ),
    path("quarters/", views.QuarterListView.as_view(), name="quarter-list"),
    path(
        "download/media/<int:media_id>/",
        views.DownloadMediaView.as_view(),
        name="download_resource",
    ),
    path(
        "change-role/",
        views.ChangeRoleView.as_view(),
        name="change-user-role",
    ),
    path(
        "download/file/<uuid:download_token>/",
        views.DownloadFileView.as_view(),
        name="download_file",
    ),
    path(
        "download/history/",
        views.DownloadHistoryView.as_view(),
        name="download_history",
    ),
    path(
        "moderator/", views.ModeratorCreateViewSet.as_view(), name="moderator"
    ),
    path(
        "moderator/resource-types/",
        views.ModeratorResourceTypesAPIView.as_view(),
        name="moderator",
    ),
    path(
        "chats/", views.ChatListCreateView.as_view(), name="chat-list-create"
    ),
    path(
        "science-info/<int:science_id>/",
        views.ModeratorCountsByScienceAndClassAPIView.as_view(),
        name="science-info",
    ),
    path("search/", UnifiedSearchView.as_view(), name="unified-search"),
    path(
        "moderator/media/",
        views.moderator_media_list,
        name="moderator-media-list",
    ),
    path(
        "weeks/",
        WeeksByQuarterView.as_view(),
        name="moderator-media-detail",
    ),
    path(
        "ai/",
        views.AiAPIView.as_view(),
        name="ai",
    ),
    path("plan/", views.PlanApiView.as_view(), name="plan"),
    path("topic/", views.TopicApiView.as_view(), name="topic"),
    path("media/", views.MediaApiView.as_view(), name="media"),
    path(
        "mobile_download_history/",
        views.MobileDownloadHistoryView.as_view(),
        name="mobile_download_history",
    ),
    path(
        "mobile_upload_history/",
        views.MobileUploadHistoryView.as_view(),
        name="mobile_upload_history",
    ),
    ############################################################################################################
    # Permission bor bo'lgan foydalanuvchilar uchun
    ############################################################################################################
    path(
        "moderator/resource-types/",
        views.ModeratorResourceTypesAPIView.as_view(),
        name="moderator",
    ),
    path(
        "moderator/science/",
        views.ModeratorScienceApiView.as_view(),
        name="moderator-science",
    ),
    path(
        "moderator/science-type/",
        views.ModeratorScienceTypeApiView.as_view(),
        name="science-type",
    ),
    path(
        "moderator/classes/",
        views.ModeratorClassesApiView.as_view(),
        name="moderator-classes",
    ),
    path(
        "moderator/class-groups/",
        ModeratorClassGroupApiView.as_view(),
        name="moderator-class-groups",
    ),
    path(
        "moderator/quarters/",
        views.ModeratorQuarterApiView.as_view(),
        name="moderator-quarters",
    ),
    path(
        "moderator/languages/",
        views.ModeratorLanguageAPIView.as_view(),
        name="moderator-languages",
    ),
    path(
        "algorithm/",
        views.AlgorithmApiView.as_view(),
        name="algorithm",
    ),
]
