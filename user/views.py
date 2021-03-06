from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.settings import api_settings

from user.models import User
from user.serializers import UserSerializer, UserListSerializer, UserUpdatePokemonSerializer


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """
    user's login/taken token
    """
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """
    managing user's data, user`s account
    """
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class ListUserView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer


class UpdateUserView(generics.RetrieveUpdateAPIView):
    """
    view for updating user`s pokemons (choosing)
    """
    serializer_class = UserUpdatePokemonSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user
