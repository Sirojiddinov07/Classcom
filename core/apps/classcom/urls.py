from django.urls import path
from django.urls import include
from rest_framework import routers

from core.apps.classcom import views

router = routers.DefaultRouter()
router.register('plan', views.PlanViewSet, basename="plan")
router.register("topic", views.TopicViewSet, basename="topic")
router.register("media", views.MediaViewSet, basename="media")
router.register("class", views.ClassesViewSet, basename="class")
router.register("science", views.ScienceViewSet, basename="science")
router.register("schedule", views.ScheduleViewSet, basename="schedule")
router.register("resource", views.ResourceViewSet, basename="resource")
router.register("moderator", views.ModeratorCreateViewSet, basename="moderator") # noqa

urlpatterns = [
    path('', include(router.urls)),
    path('download_resource/<int:resource_id>/', views.DownloadResourceView.as_view(), name='download_resource'), # noqa
    path('download_file/<uuid:download_token>/', views.DownloadFileView.as_view(), name='download_file'), # noqa
]
