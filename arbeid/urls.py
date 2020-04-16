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
from django.urls import include, path, re_path
from django.utils.safestring import mark_safe
from rest_framework import routers
from rest_framework.response import Response
from rest_framework.views import APIView

from delt.router import router as configrouter
from delt.settingsregistry import get_settings_registry
from elements.router import router as elementsrouter
from jobb.router import JobRouter
from jobb.router import router as jobrouter
from kanal.handler import KanalHandler

get_settings_registry().setHandlerForBackend("kanal", KanalHandler()) # This shouldnt be done here?

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
                   'jobs': request.build_absolute_uri('jobs/'),
                   }
        return Response(apidocs)




urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', DocsView.as_view()),
    url(r'^api/elements/', include((elementsrouter.urls, 'elementsapi'))),
    url(r'^api/config/', include((configrouter.urls, 'configapi'))),
    url(r'^api/jobs/', include((jobrouter.urls, 'jobsapi'))),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]
