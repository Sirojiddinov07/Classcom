#####################
# My Settings
#####################
INSTALLED_APPS = [
    "channels",
    "rest_framework",
    "corsheaders",
    "django_filters",
    "rosetta",
    "django_redis",
    "rest_framework_simplejwt",
    "crispy_forms",
    "django_ckeditor_5",
    "polymorphic",
    "drf_spectacular",
    #####################
    # My apps
    #####################
    "core.apps.home.apps.HomeConfig",
    "core.http.HttpConfig",
    "core.apps.accounts.apps.AccountsConfig",
    "core.console.ConsoleConfig",
    "core.apps.websocket.apps.WebsocketConfig",
    "core.apps.classcom.apps.ClassComConfig",
    "core.apps.payments.apps.PaymentsConfig",
]
