from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import *


class UserViewSet(viewsets.ModelViewSet):
    """
    Returns a list of all **active** accounts in the system.

    For more details on how accounts are activated please [see here][ref].

    [ref]: http://example.com/activating-accounts
    """
    filter_backends = (DjangoFilterBackend,)
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    """
    Returns a list of all **active** accounts in the system.

    For more details on how accounts are activated please [see here][ref].

    [ref]: http://example.com/activating-accounts
    """
    filter_backends = (DjangoFilterBackend,)
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


    @action(methods=['get'], detail=False,
            url_path='me', url_name='me')
    def me(self, request):
        # We are trying to pass on selection params
        serialized = ProfileSerializer(request.user.profile)
        return Response(serialized.data)