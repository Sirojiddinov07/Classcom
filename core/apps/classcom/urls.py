from django.urls import include, path
from django.urls import re_path
from rest_framework import routers

from core.apps.classcom import views
from core.apps.classcom.consumers import NotificationConsumer
from core.apps.classcom.views import UnifiedSearchView, WeeksByQuarterView
from core.http.views import SchoolTypeViewSet

router = routers.DefaultRouter()
router.register("plan", views.PlanViewSet, basename="plan")
router.register("topic", views.TopicViewSet, basename="topic")
router.register("media", views.MediaViewSet, basename="media")
router.register("feedback", views.FeedbackCreateViewSet, basename="feedback")
router.register("answer", views.AnswerCreateViewSet, basename="answer")
router.register("class", views.ClassesViewSet, basename="class")
router.register("science", views.ScienceViewSet, basename="science")
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

urlpatterns = [
    path("", include(router.urls)),
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
]

websocket_urlpatterns = [
    re_path(r"ws/notifications/$", NotificationConsumer.as_asgi()),
]
