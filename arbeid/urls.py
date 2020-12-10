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
import logging
from reactive.handler import ReactiveHandler
from delt.registries.handler import get_handler_registry
from vart.handler import VartHandler

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
from delt.bouncers.job.all_access import AllAccessJobBouncer
from delt.bouncers.node.all_access import AllAccessNodeBouncer
from delt.bouncers.pod.all_access import AllAccessPodBouncer
from delt.discover import (autodiscover_nodes, autodiscover_pods,
                           autodiscover_publishers, autodiscover_routers)
from delt.orchestrator import get_orchestrator
from delt.publishers.log import LogPublisher
from delt.router import router as configrouter
from delt.validators.alwaystrue import AlwaysTrueValidator
from elements.router import router as elementsrouter
from flow.router import router as flowrouter
from fremmed.handler import FremmedHandler
from fremmed.publisher import FremmedPublisher
from herre.router import router as herrerouter
from jobb.router import JobRouter
from jobb.router import router as jobrouter
from kanal.handler import KanalHandler
from konfig.backend import KonfigBackend
from port.handler import PortHandler
from port.publisher import PortPublisher
from providers.auto.handler import AutoProviderHandler

logger = logging.getLogger(__name__)

try:
    autodiscover_nodes(catalog=True)
except Exception as e:
    # TODO: For now if we are migrating this returns an error
    logger.error(f"Could not discover Nodes {e}")
     


orchestrator = get_orchestrator()


orchestrator.setPublisher("log", LogPublisher())
orchestrator.setPublisher("balder", BalderPublisher())
orchestrator.setPublisher("port", PortPublisher())


orchestrator.setHandlerForProvider("kanal", KanalHandler())
orchestrator.setHandlerForProvider("fremmed", FremmedHandler())
orchestrator.setHandlerForProvider("port", PortHandler())
orchestrator.setHandlerForProvider("auto", AutoProviderHandler())


get_handler_registry().registerHandler(VartHandler())
get_handler_registry().registerHandler(ReactiveHandler())

orchestrator.setDefaultValidator(AlwaysTrueValidator())


orchestrator.setDefaultJobBouncer(AllAccessJobBouncer)
orchestrator.setDefaultPodBouncer(AllAccessPodBouncer)
orchestrator.setDefaultNodeBouncer(AllAccessNodeBouncer)

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
                   'flows': request.build_absolute_uri('flows/'),
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
    url(r'^api/flows/', include((flowrouter.urls, 'flowsapi'))),
    url('avatar/', include('avatar.urls')),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]
