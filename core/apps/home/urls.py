"""
Home app urls
"""

from django.urls import include, path
from rest_framework import routers

from core.apps.home import views
from core.apps.home.views import change_language, DashboardView

router = routers.DefaultRouter()
router.register("", views.PostListView, basename="posts")

urlpatterns = [
    path(
        "messages/",
        views.FrontendTranslationView.as_view(),
        name="frontend-translation",
    ),  # noqa
    path("posts/", include(router.urls), name="posts"),
    path("", views.HomeView.as_view(), name="home"),
    path("admin/dashboard/", DashboardView.as_view(), name="dashboard"),
    path("change_language/", change_language, name="change_language"),
]
