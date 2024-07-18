class Role:

    def __init__(self, user) -> None:
        self.user = user
        self.groups = self.user.groups.all()
        self.groups_ids = self.groups.values_list("id", flat=True)

    def get_roles(self):
        return self.groups

    def has_group(self, groups):
        return self.groups.filter(name__in=groups).exists()

    def has_permission(self, permissions):
        return self.groups.filter(permissions__name__in=permissions)
