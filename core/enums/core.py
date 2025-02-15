from django.utils.translation import gettext as _


class Codes:
    # Database errors
    DB_CONNECTION_ERROR = 1001
    DB_SQL_EXECUTION_ERROR = 1002
    DB_READ_ERROR = 1003
    DB_WRITE_ERROR = 1004

    # Filesystem errors
    FILE_OPEN_ERROR = 2001
    FILE_WRITE_ERROR = 2002
    FILE_READ_ERROR = 2003
    FILE_DELETE_ERROR = 2004

    # Connection errors
    NETWORK_CONNECTION_ERROR = 3001
    NETWORK_HTTP_REQUEST_ERROR = 3002
    NETWORK_WEBSOCKET_ERROR = 3003

    # Programming errors
    INVALID_PARAMETER_VALUE = 4001
    REQUIRED_PARAMETER_MISSING = 4002
    CONSTRAINT_VIOLATION = 4003
    INVALID_PARAMETERS = 4006
    NOT_FOUND_ERROR = 4004
    USER_ALREADY_EXISTS_ERROR = 4005
    USER_NOT_FOUND_ERROR = 4006
    BOCKED_ERROR = 4007
    INVALID_OTP_ERROR = 4008

    # Security errors
    AUTHENTICATION_ERROR = 5001
    UNAUTHORIZED_ACCESS = 5002
    CSRF_DETECTED = 5003
    INVALID_CREDENTIALS = 5005


class Messages:
    SEND_MESSAGE = _("Sms %(phone)s raqamiga yuborildi")
    USER_ALREADY_EXISTS = _("User already exists")
    OTP_CONFIRMED = _("Tasdiqlash ko'di qabul qilindi")
    INVALID_OTP = _("Tasdiqlash ko'di xato")
    CHANGED_PASSWORD = _("Parol o'zgartirildi")
