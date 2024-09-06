from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from django.utils.translation import activate


class LanguageMiddleware(MiddlewareMixin):
    def process_request(self, request):
        language_code = request.session.get(settings.LANGUAGE_COOKIE_NAME)
        if language_code:
            activate(language_code)
