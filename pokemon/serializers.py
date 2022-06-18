from rest_framework import serializers

from pokemon.models import Pokemon


class PokemonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pokemon
        fields = ("id", "name", "url", "user")


class PokemonListSerializer(PokemonSerializer):
    pass
