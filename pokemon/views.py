from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from pokemon.models import Pokemon
from pokemon.serializers import PokemonSerializer

SOURCE_DATA = "https://pokeapi.co/api/v2/pokemon"


class PokemonViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet,
):
    queryset = Pokemon.objects.all()
    serializer_class = PokemonSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Pokemon.objects.filter(user=self.request.user)

    # def get_serializer_class(self):
    #     if self.action == "list":
    #         return PokemonSerializer
    #
    #     return PokemonSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
