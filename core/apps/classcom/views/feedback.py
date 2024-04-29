from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action

from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as __

from core.http.views import ApiResponse
from ..models import Feedback, Answer
from ..serializers import FeedbackSerializer, AnswerSerializer


class FeedbackCreateViewSet(ModelViewSet):
    serializer_class = FeedbackSerializer
    queryset = Feedback.objects.all()
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AnswerCreateViewSet(ModelViewSet,ApiResponse):
    serializer_class = AnswerSerializer
    queryset = Answer.objects.all()
    permission_classes = (IsAdminUser,)

    @action(methods=['post'], detail=True)
    def create_answer(self, request, id):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(feedback_id=id)
            return ApiResponse.success(__("Success"))
        return ApiResponse.error(__("Bad Request"))
    