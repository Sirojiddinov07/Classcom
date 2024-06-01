from django.urls import path
from django.urls import include
from rest_framework import routers

from core.apps.classcom import views
from core.http.views.region import GenerateDistrictsView

router = routers.DefaultRouter()
router.register('plan', views.PlanViewSet, basename="plan")
router.register("topic", views.TopicViewSet, basename="topic")
router.register("media", views.MediaViewSet, basename="media")
router.register("feedback", views.FeedbackCreateViewSet, basename="feedback")
router.register("answer", views.AnswerCreateViewSet, basename="answer")
router.register("notification", views.NotificationListView, basename="notification")
router.register("class", views.ClassesViewSet, basename="class")
router.register("science", views.ScienceViewSet, basename="science")
router.register("schedule", views.ScheduleViewSet, basename="schedule")
router.register("moderator", views.ModeratorCreateViewSet, basename="moderator")
router.register("days_off", views.DaysOffViewSet, basename="days_off")
router.register("resource", views.ResourceViewSet, basename="resource")


urlpatterns = [
    path('', include(router.urls)),
    path('download_resource/<int:resource_id>/', views.DownloadResourceView.as_view(), name='download_resource'), # noqa
    path('download_file/<uuid:download_token>/', views.DownloadFileView.as_view(), name='download_file'), # noqa
    path('generate-districts/<int:region_id>/', GenerateDistrictsView.as_view(), name='generate-districts'),

]
