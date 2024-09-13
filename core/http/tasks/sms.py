"""
Base celery tasks
"""

from celery import shared_task
from django.utils.translation import gettext_lazy as _

from core.services import sms_service
from core.utils import console


@shared_task
def SendConfirm(phone, code):
    try:
        service: sms_service.SendService = sms_service.SendService()
        service.send_sms(
            phone,
            _(
                "classcom.uz sayti va mobil ilovasiga ro'yxatdan o'tishingingiz uchun tasdiqlash kodi: %(code)s"
            )
            % {"code": code},
        )
        console.Console().success(f"Success: {phone}-{code}")
    except Exception as e:
        console.Console().error(
            "Error: {phone}-{code}\n\n{error}".format(
                phone=phone, code=code, error=e
            )
        )  # noqa
