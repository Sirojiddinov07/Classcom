from django.utils.translation import gettext as _
from rest_framework.exceptions import APIException

from .models import Plans


class PlanService:

    def get_plan(self):
        # TODO: Hozirgi oydagi planni olish logikasini yozish kerak
        plan = Plans.objects.all()
        if plan.exists():
            return plan.first()
        else:
            raise APIException(
                _(
                    "Serverda plan topilmadi bu texnik xatolik iltimos adminga murojat qiling"
                )
            )
