from rest_framework import serializers

from core.apps.classcom.models import TmrFiles


class TmrFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TmrFiles
        fields = (
            "id",
            "tmr_appeal",
            "title",
            "description",
            "file",
            "is_active",
            "type",
            "size",
            "created_at",
            "updated_at",
        )
        read_only_fields = ["type", "size"]

    def to_representation(self, instance):
        context = super().to_representation(instance)
        context["url"] = instance.file.url
        return context
