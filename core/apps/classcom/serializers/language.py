from rest_framework import serializers

from core.apps.classcom.choices import LanguageModel


class LanguageModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = LanguageModel
        fields = "__all__"
