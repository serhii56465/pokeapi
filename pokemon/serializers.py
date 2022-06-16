from rest_framework import serializers

from pokemon.models import Pokemon
from user.serializers import UserSerializer


class PokemonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pokemon
        fields = ("id", "name", "url")


class PokemonListSerializer(PokemonSerializer):
    pass
#     users = UserSerializer(many=True, read_only=True)
