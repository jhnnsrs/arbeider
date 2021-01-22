# Create your views here.
import re
from django.contrib.auth.models import User
from django.http.response import HttpResponse
from rest_framework import viewsets, status
from rest_framework.response import Response
from oauth2_provider.models import AccessToken


class UserPathViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving users.
    """
    def create(self, request):
        print(request.data)
        token = request.data["username"]
        thetoken = AccessToken.objects.get(token=token)
        print(thetoken)
        return HttpResponse("allow", status=status.HTTP_200_OK)


class VHostPathViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving users.
    """
    def create(self, request):
        print(request.data)

        return HttpResponse("allow", status=status.HTTP_200_OK)

class ResourcePathViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving users.
    """
    def create(self, request):
        print(request.data)

        return HttpResponse("allow", status=status.HTTP_200_OK)

class TopicPathViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving users.
    """
    def create(self, request):
        print(request.data)

        return HttpResponse("allow", status=status.HTTP_200_OK)