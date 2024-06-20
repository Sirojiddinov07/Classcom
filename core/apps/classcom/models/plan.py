from django.db import models
from django.utils.translation import gettext_lazy as __

from core.http.models import User


class Plan(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    banner = models.ImageField(upload_to="plan/banner/")
    type = models.ForeignKey(
        "ResourceType", on_delete=models.CASCADE, null=True, blank=True
    )
    hour = models.IntegerField(default=0, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    classes = models.ForeignKey("Classes", on_delete=models.CASCADE)
    quarter = models.ForeignKey("Quarter", on_delete=models.CASCADE)
    science = models.ForeignKey("Science", on_delete=models.CASCADE)
    topic = models.ForeignKey("Topic", on_delete=models.CASCADE)
    plan_resource = models.ManyToManyField("Media", blank=True, null=True)


    def __str__(self):
        return self.name


    @staticmethod
    def get_grouped_plans():
        plans = Plan.objects.all()
        grouped_plans = {}
        for plan in plans:
            key = (plan.classes, plan.quarter, plan.science)
            if key not in grouped_plans:
                grouped_plans[key] = []
            grouped_plans[key].append(plan)
        grouped_plans_list = [
            (key[0], key[1], key[2], plans) for key, plans in grouped_plans.items()
        ]
        return grouped_plans_list

    class Meta:
        verbose_name = __("Plan")
        verbose_name_plural = __("Plan")
