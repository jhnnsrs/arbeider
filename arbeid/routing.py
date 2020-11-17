from kanal.registry import get_kanal_registry
from balder.notifier.consumer import NotifyConsumer
from channels.auth import AuthMiddlewareStack
from channels.routing import ChannelNameRouter, ProtocolTypeRouter, URLRouter
from django.urls import path

from django.core.asgi import get_asgi_application
from balder.consumers import MyGraphqlWsConsumer
from balder.middleware import ApolloAuthTokenMiddleware
from delt.consumers.gateway import GatewayConsumer
from delt.registry import get_registry
from fremmed.consumers import FremmedJobConsumer, FremmedProvisionConsumer
from kanal.provisioner import KanalProvisionConsumer
from port.gateway import PortGateway
from port.provisioner import PortProvision

# The channel routing defines what connections get handled by what consumers,
# selecting on either the connection type (ProtocolTypeRouter) or properties
# of the connection's scope (like URLRouter, which looks at scope["path"])
# For more, see http://channels.readthedocs.io/en/latest/topics/routing.html
WithApolloMiddleWare = lambda inner: AuthMiddlewareStack(ApolloAuthTokenMiddleware(inner))



application = ProtocolTypeRouter({

    # Channels will do this for you automatically. It's included here as an example.
    "http": get_asgi_application(),

    # Route all WebSocket requests to our custom chat handler.
    # We actually don't need the URLRouter here, but we've put it in for
    # illustration. Also note the inclusion of the AuthMiddlewareStack to
    # add users and sessions - see http://channels.readthedocs.io/en/latest/topics/authentication.html
    'websocket': AuthMiddlewareStack(URLRouter([
        path('graphql/', MyGraphqlWsConsumer.as_asgi()),
        path('graphql', MyGraphqlWsConsumer.as_asgi()),
    ])),
    "channel": ChannelNameRouter({
        # If running in KANAL Mode
        #**get_kanal_registry().getConsumersMap(),
        "fremmed": FremmedProvisionConsumer.as_asgi(),
        "kanal": KanalProvisionConsumer.as_asgi(),
        "fremmedjob": FremmedJobConsumer.as_asgi(),
        "port": PortProvision.as_asgi(),
        "gateway": GatewayConsumer.as_asgi(),
        "portgateway": PortGateway.as_asgi(),
        "thenotifier": NotifyConsumer.as_asgi(),
        }
        ),
})
