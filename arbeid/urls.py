"""arbeid URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import include, path, re_path
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from graphql.backend import GraphQLCoreBackend
from rest_framework import routers
from rest_framework.response import Response
from rest_framework.views import APIView

from balder.publisher import BalderPublisher
from delt.publishers.log import LogPublisher
from delt.router import router as configrouter
from delt.settingsregistry import get_settings_registry
from elements.router import router as elementsrouter
from fremmed.handler import FremmedHandler
from herre.router import router as herrerouter
from jobb.router import JobRouter
from jobb.router import router as jobrouter
from kanal.handler import KanalHandler

get_settings_registry().setHandlerForBackend("kanal", KanalHandler())
get_settings_registry().setHandlerForBackend("fremmed", FremmedHandler())
get_settings_registry().setPublisher("log", LogPublisher())
get_settings_registry().setPublisher("balder", BalderPublisher())

class DocsView(APIView):
    """
    RESTFul Documentation of my app [b](http://google.de)
    """

    def get_view_name(self) -> str:
        return "Trontheim"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get(self, request, *args, **kwargs):
        apidocs = {'elements': request.build_absolute_uri('elements/'),
                   'config': request.build_absolute_uri('config/'),
                   'herre': request.build_absolute_uri('herre/'),
                   'jobs': request.build_absolute_uri('jobs/'),
                   }
        return Response(apidocs)

# Bootstrap Backend
@login_required
def index(request):
        # Render that in the index template
    return render(request, "index-oslo.html")


urlpatterns = [
    path('', index, name='index'),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^graphql$', csrf_exempt(GraphQLView.as_view(graphiql=True))),
    path('admin/', admin.site.urls),
    path('api/', DocsView.as_view()),
    url(r'^api/elements/', include((elementsrouter.urls, 'elementsapi'))),
    url(r'^api/herre/', include((herrerouter.urls, 'herrapi'))),
    url(r'^api/config/', include((configrouter.urls, 'configapi'))),
    url(r'^api/jobs/', include((jobrouter.urls, 'jobsapi'))),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]
