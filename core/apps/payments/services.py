import requests
from django.utils.translation import gettext as _
from rest_framework.exceptions import APIException
from django.utils import timezone
from logging import info

from common.env import env


class PlanService:
    def get_plan(self):
        from core.apps.payments.models import Plans

        # TODO: Implement logic to retrieve the current month's plan
        current_date = timezone.now().date()

        plan = Plans.objects.filter(
            quarter__start_date__lte=current_date,
            quarter__end_date__gte=current_date,
        ).last()

        if not plan:
            plan = Plans.objects.filter(
                quarter__start_date__gt=current_date
            ).first()

        if plan:
            return plan
        raise APIException(
            _(
                "Serverda plan topilmadi bu texnik xatolik iltimos adminga murojat qiling"
            )
        )


class UzumService:
    def __init__(self):
        self.uzum_id = env("UZUM_ID")
        self.uzum_key = env("UZUM_KEY")
        self.lang = "uz-UZ"

    def register(self, client_id, order_id, amount, detail):
        url = "https://checkout-key.inplat-tech.com/api/v1/payment/register"

        payload = {
            "successUrl": "https://my.classcom.uz/history/",
            "failureUrl": "https://my.classcom.uz/payment/",
            "viewType": "WEB_VIEW",
            "clientId": str(client_id),
            "currency": 860,
            "paymentDetails": detail,
            "orderNumber": str(order_id),
            "sessionTimeoutSecs": 600,
            "amount": 100 * 100,
            "merchantParams": {
                "divisionId": "string",
                "divisionName": "string",
                "cart": {
                    "cartId": "1212",
                    "receiptType": "PURCHASE",
                    "items": [
                        {
                            "title": "string",
                            "productId": "string",
                            "quantity": 1,
                            "unitPrice": 1,
                            "total": 1,
                            "receiptParams": {
                                "spic": "10305008002000000",
                                "packageCode": "1514296",
                                "vatPercent": 99,
                                "PINFL": "11111111111111",
                            },
                        }
                    ],
                    "total": 1,
                },
            },
            "paymentParams": {
                "operationType": "PAYMENT",
                "payType": "ONE_STEP",
                "force3ds": True,
            },
        }

        headers = {
            "X-Terminal-Id": self.uzum_id,
            "X-API-Key": self.uzum_key,
            "Content-Language": self.lang,
            "Content-Type": "application/json",
        }

        response = requests.post(url, headers=headers, json=payload)

        if response.status_code != 200:
            raise Exception("Status kod 200 emas")

        info(response.json())
        data = response.json().get("result", {})
        trans_id = data.get("orderId")
        redirect_url = data.get("paymentRedirectUrl")

        if not trans_id or not redirect_url:
            raise Exception("Ma'lumotlar kutilgan formatda emas")

        return trans_id, redirect_url
