from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from rest_framework.test import APIClient

USER_UPDATE_URL = reverse("user:manage_pokemon")
USER_REGISTER_URL = reverse("user:create")


class UnauthenticatedUserApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def testAuthRequired(self):
        res = self.client.get(USER_UPDATE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_user(self):
        payload = {
            "username": "new_user",
            "email": "test@test.com",
            "password": "123456",
        }

        res = self.client.post(USER_REGISTER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)


class AuthenticatedUserApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test", "test@test.com", "password"
        )
        self.client.force_authenticate(self.user)

    def testAuthRequired(self):
        res = self.client.get(USER_UPDATE_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
