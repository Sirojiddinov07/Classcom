from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType


class Roles:
    def run(self):
        roles = [
            {
                "name": "moderator",
                "permissions": [
                    "resource:create",
                    "resource:edit",
                    "resource:delete",
                    "resource:view",
                ],
            },
            {
                "name": "admin",
                "permissions": [
                    "plan:view",
                    "plan:create",
                    "plan:edit",
                    "plan:delete",
                ],
            },
        ]

        for role in roles:
            group, _ = Group.objects.get_or_create(name=role.get("name"))
            for permissions in role.get("permissions", []):
                permission, _ = Permission.objects.get_or_create(
                    name=permissions,
                    content_type=ContentType.objects.get_for_model(Permission),
                    codename=permissions
                )
                group.permissions.add(permission)
