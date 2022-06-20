from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from rest_framework.test import APIClient

from pokemon.models import Pokemon
from user.models import User
from user.serializers import UserUpdatePokemonSerializer

USER_UPDATE_URL = reverse("user:manage_pokemon")
USER_REGISTER_URL = reverse("user:create")


def sample_pokemon(**params):
    defaults = {
        "name": "pokemon",
        "url": "pokemon-url",
        "user": None,
    }
    defaults.update(params)

    return Pokemon.objects.create(**defaults)


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

    def testManagePokemon(self):
        another_user = get_user_model().objects.create_user(
            "test2", "test2@test.com", "password"
        )
        pokemon_none_user = sample_pokemon()
        pokemon_another_user = sample_pokemon(name="pokemon2", user=another_user)
        pokemon_auth_user = sample_pokemon(name="pokemon3", user=self.user)

        payload = {
            "username": "test",
            "email": "test@test.com",
            "is_staff": False,
            "pokemons": [pokemon_none_user.name, pokemon_another_user.name, pokemon_auth_user.name]
        }

        res = self.client.get(USER_UPDATE_URL)

        auth_user = User.objects.get(username="test")
        serializer = UserUpdatePokemonSerializer(auth_user)

        self.assertEqual(res.data, serializer.data)

        patch_res = self.client.patch(USER_UPDATE_URL, payload)

        auth_user = User.objects.get(username="test")
        serializer2 = UserUpdatePokemonSerializer(auth_user, payload)

        if serializer2.is_valid():
            self.assertEqual(patch_res.data, serializer2.data)
