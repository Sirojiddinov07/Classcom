from django.urls import path, include
from core.apps.classcom import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register("topic", views.TopicViewSet, basename="topic")
router.register("science", views.ScienceViewSet, basename="science")
router.register("class", views.ClassesViewSet, basename="class")
router.register("resource", views.ResourceViewSet, basename="resource")
router.register("media", views.MediaViewSet, basename="media")

urlpatterns = [
    path('', include(router.urls)),
]
