from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.apps.classcom.models import Plan, Moderator
from core.apps.classcom.permissions import PlanPermission
from core.apps.classcom.serializers import PlanSerializer, PlanDetailSerializer


class PlanApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        plan_serializer = PlanSerializer(
            data=request.data, context={"request": request}
        )
        plan_serializer.is_valid(raise_exception=True)
        self.permission_classes.append(PlanPermission(["moderator"]))
        plan_serializer.save()
        return Response(plan_serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):
        user = request.user
        plan_id = request.query_params.get("id", None)

        if Moderator.objects.filter(user=user).exists():
            plans = Plan.objects.filter(user=user)
        else:
            plans = Plan.objects.all()

        if plan_id:
            plans = plans.filter(id=plan_id)

        plan_serializer = PlanDetailSerializer(plans, many=True)
        return Response(plan_serializer.data, status=status.HTTP_200_OK)

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
