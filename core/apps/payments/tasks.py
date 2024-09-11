from celery import shared_task

from .models import Orders
from .services import PlanService


@shared_task
def update_price_task(order_id):
    try:
        order = Orders.objects.get(id=order_id)
        plan = PlanService().get_plan()
        order.price = plan.price * order.types.all().count()
        order.end_date = plan.quarter.end_date
        order.save(update_fields=["price", "end_date"])
        print("====================================")
    except Orders.DoesNotExist:
        # Handle the case where the order does not exist
        pass
