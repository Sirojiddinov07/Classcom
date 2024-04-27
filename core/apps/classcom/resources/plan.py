from import_export import resources

from core.apps.classcom import models


class PlanResource(resources.ModelResource):
    """
    Import data from Excel
    """
    class Meta:
        model = models.Plan
        fields = (
            'id',
            'classes',
            'topic',
            'hour'
        )

    def before_import_row(self, row, **kwargs):
        name = row.get('topic')
        quarter = row.pop('quarter')
        science = row.pop('science')
        (topic, _created) = models.Topic.objects.get_or_create(
            name=name,
            quarter_id=quarter,
            science_id=science
        )
        row['topic'] = topic.id
