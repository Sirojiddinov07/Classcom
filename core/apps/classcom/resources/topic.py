from import_export import resources

from core.apps.classcom.models import Topic


class TopicResource(resources.ModelResource):
    class Meta:
        model = Topic
        fields = (
            "id",
            "sequence_number",
            "weeks",
            "name",
            "description",
            "hours",
            "plan_id",
        )
