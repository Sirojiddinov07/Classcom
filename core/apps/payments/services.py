from django.utils.translation import gettext as _
from rest_framework.exceptions import APIException
import requests
from common.env import env
from .models import Plans


class PlanService:
    def get_plan(self):
        # TODO: Implement logic to retrieve the current month's plan
        plan = Plans.objects.first()
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
        url = "https://test-chk-api.uzumcheckout.uz/api/v1/payment/register"

        payload = {
            "successUrl": "https://api.classcom.uz/webhook/uzum/",
            "failureUrl": "https://api.classcom.uz/webhook/uzum/",
            "viewType": "WEB_VIEW",
            "clientId": str(client_id),
            "currency": 860,
            "paymentDetails": detail,
            "orderNumber": str(order_id),
            "sessionTimeoutSecs": 600,
            "amount": amount,
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
                            "quantity": 0,
                            "unitPrice": 0,
                            "total": 0,
                            "receiptParams": {
                                "spic": "10305008002000000",
                                "packageCode": "1514296",
                                "vatPercent": 99,
                                "PINFL": "11111111111111",
                            },
                        }
                    ],
                    "total": 0,
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

        data = response.json().get("result", {})
        trans_id = data.get("orderId")
        redirect_url = data.get("paymentRedirectUrl")

        if not trans_id or not redirect_url:
            print(response.content)
            raise Exception("Ma'lumotlar kutilgan formatda emas")

        return trans_id, redirect_url
