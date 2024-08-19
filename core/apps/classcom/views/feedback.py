from django.utils.translation import gettext as __
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from core.http.views import ApiResponse
from ..models import Answer, Feedback
from ..serializers import AnswerSerializer, FeedbackSerializer


class FeedbackCreateViewSet(ModelViewSet):
    serializer_class = FeedbackSerializer
    queryset = Feedback.objects.all()
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AnswerCreateViewSet(ModelViewSet, ApiResponse):
    serializer_class = AnswerSerializer
    queryset = Answer.objects.all()
    permission_classes = (IsAdminUser,)

    @action(methods=["post"], detail=True)
    def create_answer(self, request, id):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(feedback_id=id)
            return ApiResponse.success(__("Success"))
        return ApiResponse.error(__("Bad Request"))
