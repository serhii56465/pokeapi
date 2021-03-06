import requests
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from pokemon.models import Pokemon
from pokemon.serializers import PokemonSerializer, PokemonListSerializer

# Source data for uploading pokemons
SOURCE_DATA = "https://pokeapi.co/api/v2/pokemon"
PAYLOAD = {'limit': 3}


class PokemonViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet,
):
    queryset = Pokemon.objects.all()
    serializer_class = PokemonSerializer

    # delete "params" for uploading all data from source
    response_ = requests.get(SOURCE_DATA, params=PAYLOAD)
    pars_data = response_.json()
    pokemons_list = pars_data["results"]

    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == "list":
            return PokemonListSerializer

        return PokemonSerializer

    def create(self, request, pokemons_list=pokemons_list, *args, **kwargs):
        """
        Endpoint for uploading pokemons from source - use one time for each source
        """

        batch = [Pokemon(name=pokemon["name"], url=pokemon["url"]) for pokemon in pokemons_list]

        Pokemon.objects.bulk_create(batch)
        return Response()
