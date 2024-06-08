"""
All urls configurations tree
"""

from django.urls import path
from django.urls import include
from django.urls import re_path
from django.conf import settings
from django.contrib import admin
from django.views.static import serve

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("rosetta/", include("rosetta.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("i18n/", include("django.conf.urls.i18n")),
    path("", include("core.apps.accounts.urls")),
    path("", include("core.apps.home.urls")),
    path("", include("core.apps.classcom.urls")),
    path(
        "ckeditor5/",
        include("django_ckeditor_5.urls"),
        name="ck_editor_5_upload_file",
    ),  # noqa
    path("i18n/", include("django.conf.urls.i18n")),
    # Internal apps
    path("", include("core.apps.accounts.urls")),
    path("", include("core.apps.home.urls")),
    # Media and static files
    re_path(
        r"static/(?P<path>.*)", serve, {"document_root": settings.STATIC_ROOT}
    ),  # noqa
    re_path(
        r"media/(?P<path>.*)", serve, {"document_root": settings.MEDIA_ROOT}
    ),  # noqa
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]
