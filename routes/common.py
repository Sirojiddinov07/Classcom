"""
All urls configurations tree
"""

from django.conf import settings
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import include, path, re_path
from django.views.static import serve
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path("", include("core.apps.home.urls")),
    path("admin/", admin.site.urls),
    path("rosetta/", include("rosetta.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("i18n/", include("django.conf.urls.i18n")),
    path("", include("core.apps.payments.urls")),
    path("", include("core.apps.accounts.urls")),
    path("", include("core.apps.classcom.urls")),
    path(
        "ckeditor5/",
        include("django_ckeditor_5.urls"),
        name="ck_editor_5_upload_file",
    ),  # noqa
    path("i18n/", include("django.conf.urls.i18n")),
    # Media and static files
    re_path(
        r"static/(?P<path>.*)", serve, {"document_root": settings.STATIC_ROOT}
    ),  # noqa
    re_path(
        r"media/(?P<path>.*)", serve, {"document_root": settings.MEDIA_ROOT}
    ),  # noqa
    # path(
    #     "schema/", login_required(SpectacularAPIView.as_view()), name="schema"
    # ),
    path(
        "swagger/",
        login_required(
            SpectacularSwaggerView.as_view(url_name="schema"),
            login_url="/admin/",
        ),
        name="swagger-ui",
    ),
    path(
        "redoc/",
        login_required(
            SpectacularRedocView.as_view(url_name="schema"),
            login_url="/admin/",
        ),
        name="redoc",
    ),
]
