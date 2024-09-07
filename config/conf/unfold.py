from django.templatetags.static import static

# from django.urls import reverse_lazy
# from django.utils.translation import gettext_lazy as _
from . import navigation

UNFOLD = {
    "SITE_TITLE": "CLASSCOM.UZ",
    "SITE_HEADER": "CLASSCOM.UZ",
    "SITE_URL": "/",
    "SITE_ICON": {
        "light": lambda request: static("images/classcom.png"),  # light mode
        "dark": lambda request: static("images/classcom.png"),  # dark mode
    },
    "SITE_FAVICONS": [
        {
            "rel": "icon",
            "sizes": "32x32",
            "type": "image/svg+xml",
            "href": lambda request: static("images/classcom.png"),
        },
    ],
    # "SITE_LOGO": {
    #     "light": lambda request: static("images/felix.png"),  # light mode
    #     "dark": lambda request: static("images/felix.png"),  # dark mode
    # },
    "SITE_SYMBOL": "speed",  # symbol from icon set
    "SHOW_HISTORY": True,  # show/hide "History" button, default: True
    "SHOW_VIEW_ON_SITE": True,
    "LOGIN": {
        "image": lambda request: static("images/login.png"),
    },
    # "THEME": "dark",
    "STYLES": [
        lambda request: static("css/tailwind.css"),
    ],
    # "SCRIPTS": [
    # lambda request: static("js/script.js"),
    # ],
    "COLORS": {
        "font": {
            "subtle-light": "107 114 128",
            "subtle-dark": "156 163 175",
            "default-light": "75 85 99",
            "default-dark": "209 213 219",
            "important-light": "17 24 39",
            "important-dark": "243 244 246",
        },
        "primary": {
            "50": "51 97 179",
            "100": "51 97 179",
            "200": "51 97 179",
            "300": "51 97 179",
            "400": "51 97 179",
            "500": "51 97 179",
            "600": "51 97 179",
            "700": "51 97 179",
            "800": "51 97 179",
            "900": "51 97 179",
            "950": "51 97 179",
        },
    },
    "EXTENSIONS": {
        "modeltranslation": {
            "flags": {
                "uz": "🇺🇿",
                "ru": "🇷🇺",
                "en": "🇬🇧",
            },
        },
    },
    "SIDEBAR": {
        "show_search": True,  # Search in applications and models names
        "show_all_applications": True,
        "navigation": navigation.PAGES,
    },
}
