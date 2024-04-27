from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from ..models import Feedback
from ..serializers import FeedbackSerializer, AnswerSerializer


class FeedbackCreateView(CreateAPIView):
    serializer_class = FeedbackSerializer
    queryset = Feedback.objects.all()
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AnswerCreateView(CreateAPIView):
    serializer_class = AnswerSerializer
    queryset = Feedback.objects.all()
    permission_classes = (IsAdminUser,)
    lookup_field = 'id'

    def perform_create(self, serializer):
        id = self.kwargs['id']
        try:
            feedback = Feedback.objects.get(id=id)
            serializer.save(feedback=feedback)
        except Feedback.DoesNotExist:
            raise Response({"message": "Feedback does not exists", "status": 404})
    