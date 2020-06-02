from channels.auth import AuthMiddlewareStack
from channels.routing import ChannelNameRouter, ProtocolTypeRouter, URLRouter
from django.urls import path

from balder.consumers import MyGraphqlWsConsumer
from balder.middleware import ApolloAuthTokenMiddleware
from delt.consumers.gateway import GatewayConsumer
from delt.registry import get_registry
from fremmed.consumers import FremmedJobConsumer, FremmedProvisionConsumer
from kanal.provisioner import KanalProvisionConsumer
from port.provisioner import PortProvision

# The channel routing defines what connections get handled by what consumers,
# selecting on either the connection type (ProtocolTypeRouter) or properties
# of the connection's scope (like URLRouter, which looks at scope["path"])
# For more, see http://channels.readthedocs.io/en/latest/topics/routing.html
WithApolloMiddleWare = lambda inner: AuthMiddlewareStack(ApolloAuthTokenMiddleware(inner))



application = ProtocolTypeRouter({

    # Channels will do this for you automatically. It's included here as an example.
    # "http": AsgiHandler,

    # Route all WebSocket requests to our custom chat handler.
    # We actually don't need the URLRouter here, but we've put it in for
    # illustration. Also note the inclusion of the AuthMiddlewareStack to
    # add users and sessions - see http://channels.readthedocs.io/en/latest/topics/authentication.html
    'websocket': WithApolloMiddleWare(URLRouter([
        path('graphql/', MyGraphqlWsConsumer),
        path('graphql', MyGraphqlWsConsumer),
    ])),
    "channel": ChannelNameRouter({
        **get_registry().getConsumersMap(),
        "fremmed": FremmedProvisionConsumer,
        "kanal": KanalProvisionConsumer,
        "fremmedjob": FremmedJobConsumer,
        "port": PortProvision,
        "gateway": GatewayConsumer
        }
        ),
})
