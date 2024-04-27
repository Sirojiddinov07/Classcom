from django.urls import path
from django.urls import include
from rest_framework import routers

from core.apps.classcom import views

router = routers.DefaultRouter()
router.register("topic", views.TopicViewSet, basename="topic")
router.register("science", views.ScienceViewSet, basename="science")
router.register("class", views.ClassesViewSet, basename="class")
router.register("resource", views.ResourceViewSet, basename="resource")
router.register("media", views.MediaViewSet, basename="media")
router.register("schedule", views.ScheduleViewSet, basename="schedule")
router.register("moderator", views.ModeratorViewSet, basename="moderator")

urlpatterns = [
    path('', include(router.urls)),
]
