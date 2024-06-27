from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from core.apps.classcom.models import Moderator
from core.apps.classcom.serializers import ModeratorCreateSerializer


class ModeratorCreateViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_successful_moderator_creation(self):
        data = {
            "first_name": "string",
            "last_name": "string",
            "phone": "998946593659",
            "password": "string1212",
            "region": 1,
            "district": 1,
            "institution": "OLIY",
            "institution_number": "string",
            "science": 1,
            "classes": 1,
            "degree": "HIGHER",
            "docs": "string",
        }
        response = self.client.post(
            "core/apps/classcom/views/moderator.py", data=data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Moderator.objects.count(), 1)
        self.assertEqual(Moderator.objects.get().name, data["name"])

    def test_moderator_creation_with_invalid_data(self):
        data = {}
        response = self.client.post(
            "core/apps/classcom/views/moderator.py", data=data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Moderator.objects.count(), 0)
