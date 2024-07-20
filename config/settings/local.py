from common.env import env  # noqa
from config.settings.common import *  # noqa
from config.settings.common import (
    ALLOWED_HOSTS,
    INSTALLED_APPS,
    MIDDLEWARE,
    REST_FRAMEWORK,
)

DATABASES = {
    "default": {
        "ENGINE": env.str("DB_ENGINE"),
        "NAME": env.str("DB_NAME"),
        "USER": env.str("DB_USER"),
        "PASSWORD": env.str("DB_PASSWORD"),
        "HOST": env.str("DB_HOST"),
        "PORT": env.str("DB_PORT"),
    }
}

MIDDLEWARE += [
    "core.middlewares.ExceptionMiddleware",
]

INSTALLED_APPS += ["django_extensions"]

# Allowed Hosts
ALLOWED_HOSTS += ["127.0.0.1", "192.168.100.26"]

REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"] = {
    "user": "10/min",
}
