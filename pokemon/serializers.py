from rest_framework import serializers

from pokemon.models import Pokemon


class PokemonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pokemon
        fields = ("id", "name", "url")

    def create(self, validated_data):
        pokemon = Pokemon.objects.create(**validated_data)
        return pokemon


# class PokemonListSerializer(PokemonSerializer):
