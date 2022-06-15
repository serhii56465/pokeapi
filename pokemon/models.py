from django.conf import settings
from django.db import models


class Pokemon(models.Model):
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="pokemons",
        null=True
    )
