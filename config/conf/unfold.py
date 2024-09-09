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
            "50": "65 144 176",
            "100": "65 144 176",
            "200": "65 144 176",
            "300": "65 144 176",
            "400": "65 144 176",
            "500": "65 144 176",
            "600": "65 144 176",
            "700": "65 144 176",
            "800": "65 144 176",
            "900": "65 144 176",
            "950": "65 144 176",
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
