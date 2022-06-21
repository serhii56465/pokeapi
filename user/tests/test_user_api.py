from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from rest_framework.test import APIClient

from pokemon.models import Pokemon
from pokemon.serializers import PokemonSerializer
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

    def test_auth_required(self):
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

    def test_auth_required(self):
        res = self.client.get(USER_UPDATE_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_manage_pokemon(self):
        another_user = get_user_model().objects.create_user(
            "test2", "test2@test.com", "password"
        )
        pokemon_none_user = sample_pokemon()
        pokemon_another_user = sample_pokemon(name="pokemon2", user=another_user)
        pokemon_auth_user = sample_pokemon(name="pokemon3", user=self.user)
        pokemon_none2_user = sample_pokemon(name="pokemon4")

        payload = {
            "username": "test",
            "email": "test@test.com",
            "is_staff": False,
            "pokemons": [
                pokemon_none_user.name,
                pokemon_another_user.name,
                pokemon_auth_user.name,
                pokemon_none2_user.name
            ]
        }

        res = self.client.patch(USER_UPDATE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        pokemon_3_after = Pokemon.objects.get(name="pokemon3")
        serializer_pokemon_3_after = PokemonSerializer(pokemon_3_after)

        self.assertEqual(serializer_pokemon_3_after.data["user"], None)

        auth_user = User.objects.get(username="test")
        serializer_auth_user = UserUpdatePokemonSerializer(auth_user)

        self.assertEqual(res.data, serializer_auth_user.data)
        self.assertEqual(serializer_auth_user.data["pokemons"], ["pokemon", "pokemon4"])

        another_user_test2 = User.objects.get(username="test2")
        serializer_another_user = UserUpdatePokemonSerializer(another_user_test2)

        self.assertEqual(serializer_another_user.data["pokemons"], ["pokemon2"])
