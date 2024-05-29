"""
Django REST Framework
"""

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    # Barcha apilar uchun majburiy authorizatsiya
    # Chetlab o'tish uchun view classga permission_classes
    # AllowAny permissionidan foydalaning
}
