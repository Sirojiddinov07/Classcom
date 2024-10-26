"""
Base celery tasks
"""

from celery import shared_task
from django.utils.translation import gettext as _

from core.services import sms_service
from core.utils import console


@shared_task
def send_congratulation_sms(phone, first_name, last_name):
    try:
        service: sms_service.SendService = sms_service.SendService()
        service.send_sms(
            phone,
            _(
                "Assalomu alaykum %(first_name)s %(last_name)s %(father_name)s sizni https://classcom.uz "
                "o’qituvchining virtual kаbinetida muallif sifatida tasdiqlanganingiz bilan tabriklaymiz!!!"
            )
            % {"first_name": first_name, "last_name": last_name},
        )
        console.Console().success(f"Success: {phone}-{first_name}-{last_name}")
    except Exception as e:
        console.Console().error(
            "Error: {phone}-{first_name}-{last_name}\n\n{error}".format(
                phone=phone,
                first_name=first_name,
                last_name=last_name,
                error=e,
            )
        )  # noqa
