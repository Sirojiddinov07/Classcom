from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.apps.classcom.models import Plan, Moderator
from core.apps.classcom.permissions import PlanPermission
from core.apps.classcom.serializers import PlanSerializer, PlanDetailSerializer
from core.apps.classcom.views import CustomPagination


class PlanApiView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def post(self, request, *args, **kwargs):
        # self.permission_classes.append(PlanPermission(["moderator"]))
        plan_serializer = PlanSerializer(
            data=request.data, context={"request": request}
        )
        plan_serializer.is_valid(raise_exception=True)
        plan_serializer.save()
        return Response(plan_serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):
        user = request.user
        plan_id = request.query_params.get("id", None)
        classes = request.query_params.get("classes", None)
        quarter = request.query_params.get("quarter", None)
        science = request.query_params.get("science", None)
        class_group = request.query_params.get("class_group", None)
        science_types = request.query_params.get("science_types", None)

        if Moderator.objects.filter(user=user).exists():
            moderator = Moderator.objects.get(user=user)
            plans = Plan.objects.filter(
                classes__in=moderator.classes.all(),
                quarter__in=moderator.quarters.all(),
                science__in=moderator.science.all(),
                class_group__in=moderator.class_groups.all(),
                science_type__in=moderator.science_type.all(),
            )
        else:
            plans = Plan.objects.filter(user=user)

        if plan_id:
            plans = plans.filter(id=plan_id)
        if classes:
            plans = plans.filter(classes=classes)
        if quarter:
            plans = plans.filter(quarter=quarter)
        if science:
            plans = plans.filter(science=science)
        if class_group:
            plans = plans.filter(class_group=class_group)
        if science_types:
            plans = plans.filter(science_types=science_types)

        paginator = self.pagination_class()
        paginated_plans = paginator.paginate_queryset(plans, request)
        plan_serializer = PlanDetailSerializer(paginated_plans, many=True)
        return paginator.get_paginated_response(plan_serializer.data)

    def patch(self, request, *args, **kwargs):
        plan_id = request.query_params.get("id", None)
        try:
            plan = Plan.objects.get(id=plan_id, user=request.user)
        except Plan.DoesNotExist:
            raise NotFound("Plan not found")
        self.permission_classes.append(PlanPermission(["moderator"]))
        plan_serializer = PlanSerializer(plan, data=request.data, partial=True)
        plan_serializer.is_valid(raise_exception=True)
        plan_serializer.save()
        return Response(plan_serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        plan_id = request.query_params.get("id", None)
        try:
            plan = Plan.objects.get(id=plan_id, user=request.user)
        except Plan.DoesNotExist:
            raise NotFound(
                "Plan not found or you do not have permission to delete it"
            )
        self.permission_classes.append(PlanPermission(["moderator"]))
        plan.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
