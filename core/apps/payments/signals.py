from django.db.models.signals import post_save

from .models import Orders
from .services import PlanService


def order_create(sender, instance, created, **kwargs):
    """Order post save signal"""
    if created:
        plan = PlanService().get_plan()
        instance.price = plan.price
        instance.end_date = plan.quarter.end_date
        instance.save()
        print("Order created")


post_save.connect(order_create, Orders)
