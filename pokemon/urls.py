from django.urls import path, include
from rest_framework import routers

from pokemon.views import PokemonViewSet

router = routers.DefaultRouter()
router.register("pokemons", PokemonViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "pokemon"
