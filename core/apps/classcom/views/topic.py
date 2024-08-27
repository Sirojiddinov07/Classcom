from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.apps.classcom.models import Topic, Plan
from core.apps.classcom.serializers.topic import (
    TopicSerializer,
    TopicDetailSerializer,
)
from core.apps.classcom.views import CustomPagination


class TopicApiView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get(self, request):
        plan_id = request.query_params.get("plan_id")
        topic_id = request.query_params.get("id")

        if topic_id:
            try:
                topic = Topic.objects.get(id=topic_id)
                serializer = TopicDetailSerializer(topic)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Topic.DoesNotExist:
                return Response(
                    {"error": "Topic not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )

        if plan_id:
            try:
                plan = Plan.objects.get(id=plan_id, user=request.user)
                topics = plan.topic.all()
                paginator = self.pagination_class()
                paginated_topics = paginator.paginate_queryset(topics, request)
                serializer = TopicDetailSerializer(paginated_topics, many=True)
                return paginator.get_paginated_response(serializer.data)
            except Plan.DoesNotExist:
                return Response(
                    {"error": "Plan not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )

        return Response(
            {"error": "Either id or plan_id is required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def post(self, request):
        plan_id = request.query_params.get("plan_id")
        if not plan_id:
            return Response(
                {"error": "plan_id is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            plan = Plan.objects.get(id=plan_id, user=request.user)
        except Plan.DoesNotExist:
            return Response(
                {"error": "Plan not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = TopicSerializer(data=request.data, many=True)
        if serializer.is_valid():
            topics = serializer.save()
            plan.topic.add(*topics)
            plan.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        topic_id = request.query_params.get("id")
        if not topic_id:
            return Response(
                {"error": "id is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            topic = Topic.objects.get(id=topic_id)
            topic.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Topic.DoesNotExist:
            return Response(
                {"error": "Topic not found"}, status=status.HTTP_404_NOT_FOUND
            )

    def patch(self, request):
        topic_id = request.query_params.get("id")
        if not topic_id:
            return Response(
                {"error": "id is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            topic = Topic.objects.get(id=topic_id)
        except Topic.DoesNotExist:
            return Response(
                {"error": "Topic not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = TopicSerializer(topic, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
