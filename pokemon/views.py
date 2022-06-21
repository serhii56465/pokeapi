import requests
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from pokemon.models import Pokemon
from pokemon.serializers import PokemonSerializer, PokemonListSerializer

SOURCE_DATA = "https://pokeapi.co/api/v2/pokemon"
PAYLOAD = {'limit': 3}


class PokemonViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet,
):
    queryset = Pokemon.objects.all()
    serializer_class = PokemonSerializer

    response_ = requests.get(SOURCE_DATA, params=PAYLOAD)
    pars_data = response_.json()
    pokemons_list = pars_data["results"]

    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == "list":
            return PokemonListSerializer

        return PokemonSerializer

    def create(self, request, pokemons_list=pokemons_list, *args, **kwargs):
        for pokemon in pokemons_list:
            serializer = self.get_serializer(data=pokemon)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
        return Response()
