from import_export import resources

from core.http.models import District, Region, ScienceGroups


class RegionResource(resources.ModelResource):
    class Meta:
        model = Region
        fields = ("region",)
        import_id_fields = ["region"]
        exclude = ("id",)


class DistrictResource(resources.ModelResource):
    class Meta:
        model = District
        fields = ("district", "region")
        import_id_fields = ["district"]
        exclude = ("id",)


class ScienceGroupsResource(resources.ModelResource):
    class Meta:
        model = ScienceGroups
        fields = ("name",)
        import_id_fields = ["name"]
        exclude = ("id",)
