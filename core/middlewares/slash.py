from django.conf import settings
from django.http import HttpResponsePermanentRedirect
from django.utils.deprecation import MiddlewareMixin


class AppendSlashWithoutRedirect(MiddlewareMixin):
    def process_request(self, request):
        excluded_paths = ["/webkook/uzum"]

        # Check if APPEND_SLASH is True and if the current path is excluded
        if (
            settings.APPEND_SLASH
            and not request.path.endswith("/")
            and request.path not in excluded_paths
        ):
            return None  # Do not append slash

        # Default behavior for other URLs
        if (
            settings.APPEND_SLASH
            and not request.path.endswith("/")
            and not request.path.endswith((".html", ".json", ".xml"))
        ):
            return HttpResponsePermanentRedirect(f"{request.path}/")
