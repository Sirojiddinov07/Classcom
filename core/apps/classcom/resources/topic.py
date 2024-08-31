from import_export import resources, fields

from core.apps.classcom.models import Topic, Plan


class TopicResource(resources.ModelResource):
    plan_id = fields.Field(column_name="plan_id")

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

    def before_import_row(self, row, row_number=None, **kwargs):
        self.plan_id = row.get("plan_id")

    def after_save_instance(self, instance, using_transactions, dry_run):
        if hasattr(self, "plan_id") and self.plan_id:
            try:
                plan = Plan.objects.get(id=self.plan_id)
                plan.topic.add(instance)
                plan.save()
            except Plan.DoesNotExist:
                pass
