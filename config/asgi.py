import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

from common.env import env  # noqa
from core.apps.classcom.urls import websocket_urlpatterns
from core.middlewares.websocket import JWTAuthMiddlewareStack

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

asgi_application = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": asgi_application,
        "websocket": JWTAuthMiddlewareStack(URLRouter(websocket_urlpatterns)),
    }
)
