from django.urls import include, path
from rest_framework import routers

from core.apps.classcom import views

# from core.apps.classcom.views import science_info

router = routers.DefaultRouter()
router.register("plan", views.PlanViewSet, basename="plan")
router.register("topic", views.TopicViewSet, basename="topic")
router.register("media", views.MediaViewSet, basename="media")
router.register("feedback", views.FeedbackCreateViewSet, basename="feedback")
router.register("answer", views.AnswerCreateViewSet, basename="answer")
router.register(
    "notification", views.NotificationListView, basename="notification"
)
router.register("class", views.ClassesViewSet, basename="class")
router.register("science", views.ScienceViewSet, basename="science")
router.register("schedule", views.ScheduleViewSet, basename="schedule")
router.register("days_off", views.DaysOffViewSet, basename="days_off")
router.register("resource", views.ResourceViewSet, basename="resource")
router.register("region", views.RegionViewSet, basename="region")
router.register("district", views.DistrictViewSet, basename="district")
router.register("types", views.ResourceTypesViewSet, basename="types")

urlpatterns = [
    path("", include(router.urls)),
    path("quarters/", views.QuarterListView.as_view(), name="quarter-list"),
    path(
        "download_resource/<int:resource_id>/",
        views.DownloadResourceView.as_view(),
        name="download_resource",
    ),
    path(
        "change-role/",
        views.ChangeRoleView.as_view(),
        name="change-user-role",
    ),
    path(
        "download_file/<uuid:download_token>/",
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
        "get-schedule/",
        views.GetScheduleDataView.as_view(),
        name="get_schedule_data",
    ),
    path(
        "get-day-schedule/",
        views.DayScheduleView.as_view(),
        name="get_day_schedule",
    ),
    path(
        "get-days-schedule/",
        views.RangeScheduleView.as_view(),
        name="get_range_schedule",
    ),
    path(
        "chats/", views.ChatListCreateView.as_view(), name="chat-list-create"
    ),
    path(
        "science-info/<int:science_id>/",
        views.ModeratorCountsByScienceAndClassAPIView.as_view(),
        name="science-info",
    ),
    path("search/", views.UnifiedSearchView.as_view(), name="unified-search"),
]
