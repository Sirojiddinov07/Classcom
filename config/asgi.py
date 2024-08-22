import os

import django
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

from core.middlewares.websocket import JWTAuthMiddlewareStack  # noqa

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

django.setup()

from core.apps.websocket.urls import websocket_urlpatterns  # noqa

asgi_application = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": asgi_application,
        "websocket": JWTAuthMiddlewareStack(URLRouter(websocket_urlpatterns)),
    }
)
