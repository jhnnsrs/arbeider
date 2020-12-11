from delt.registries.handler import get_handler_registry
from delt.registries.additionals import get_additionals_registry
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
from kanal.provisioner import KanalProvisionConsumer

# The channel routing defines what connections get handled by what consumers,
# selecting on either the connection type (ProtocolTypeRouter) or properties
# of the connection's scope (like URLRouter, which looks at scope["path"])
# For more, see http://channels.readthedocs.io/en/latest/topics/routing.html
WithApolloMiddleWare = lambda inner: AuthMiddlewareStack(ApolloAuthTokenMiddleware(inner))


pausedApps = None


handlers = get_handler_registry().getConsumerMap()
additionals = get_additionals_registry().getConsumerMap(exclude=pausedApps)

application = ProtocolTypeRouter({

    # Channels will do this for you automatically. It's included here as an example.
    "http": get_asgi_application(),

    # Route all WebSocket requests to our custom chat handler.
    # We actually don't need the URLRouter here, but we've put it in for
    # illustration. Also note the inclusion of the AuthMiddlewareStack to
    # add users and sessions - see http://channels.readthedocs.io/en/latest/topics/authentication.html
    'websocket': WithApolloMiddleWare(URLRouter([
        path('graphql/', MyGraphqlWsConsumer.as_asgi()),
        path('graphql', MyGraphqlWsConsumer.as_asgi()),
    ])),
    "channel": ChannelNameRouter({
        # If running in KANAL Mode
        #**get_kanal_registry().getConsumersMap(),
        "kanal": KanalProvisionConsumer.as_asgi(),
        "gateway": GatewayConsumer.as_asgi(),
        "thenotifier": NotifyConsumer.as_asgi(),
        **handlers,
        **additionals
    }
    ),
})
