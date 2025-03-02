from rest_framework import serializers

from ..models.feedback import Feedback


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ("user", "body", "feedback_type", "answered")

        extra_kwargs = {
            "user": {"read_only": True},
            "feedback_type": {"read_only": True},
        }


class AnswerSerializer(serializers.Serializer):
    feedback = serializers.CharField(read_only=True)
    body = serializers.CharField()
