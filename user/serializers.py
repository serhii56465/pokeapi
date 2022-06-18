from django.contrib.auth import get_user_model
from rest_framework import serializers

from pokemon.models import Pokemon


class UserSerializer(serializers.ModelSerializer):
    pokemons = serializers.SlugRelatedField(many=True, read_only=True, slug_field="name")

    class Meta:
        model = get_user_model()
        fields = ("id", "username", "email", "password", "is_staff", "pokemons")
        read_only_fields = ("is_staff", "pokemons")
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update a user, set the password correctly and return it"""
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()

        return user


class UserListSerializer(serializers.ModelSerializer):
    pokemons = serializers.SlugRelatedField(many=True, read_only=True, slug_field="name")

    class Meta:
        model = get_user_model()
        fields = ("id", "username", "email", "password", "is_staff", "pokemons")
        read_only_fields = ("is_staff",)
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}


class UserUpdatePokemonSerializer(serializers.ModelSerializer):
    pokemons = serializers.SlugRelatedField(many=True, read_only=False, slug_field="id", queryset=Pokemon.objects.all())

    class Meta:
        model = get_user_model()
        fields = ("id", "username", "email", "is_staff", "pokemons")
        read_only_fields = ("is_staff", "username", "email")

    def update(self, instance, validated_data):
        pokemons_data = validated_data.pop("pokemons", None)
        user = super().update(instance, validated_data)
        for pokemon_ in pokemons_data:
            if pokemon_.user is None:
                setattr(pokemon_, "user", user)
                pokemon_.save()
            elif pokemon_.user == user:
                setattr(pokemon_, "user", None)
                pokemon_.save()
        return user
