from django.db import close_old_connections
from urllib.parse import parse_qs
import logging
from django.conf import settings
from django.test.client import RequestFactory 
import re
from rest_framework.settings import api_settings
from channels.db import database_sync_to_async

tokenreg = re.compile(r".*token=(?P<token>.*)\'")
logger = logging.getLogger()

@database_sync_to_async
def get_user(authenticator, request):
    return authenticator.authenticate(request)



class ApolloAuthTokenMiddleware:
    """
    Custom middleware (insecure) that takes user IDs from the query string.
    """

    def __init__(self, inner):
        # Store the ASGI application we were passed
        self.inner = inner

    def __call__(self, scope):
        return ApolloAuthTokenMiddlewareInstance(scope, self)

class ApolloAuthTokenMiddlewareInstance:
    """
    Custom middleware (insecure) that takes tokens from the query string.
    """

    def __init__(self, scope, middleware):
        # Store the ASGI application we were passed
        self.middleware = middleware
        self.scope = dict(scope)
        self.inner = self.middleware.inner

    async def __call__(self, receive, send):

        # Close old database connections to prevent usage of timed out connections

        # Look up user from query string (you should also do things like
        # check it's a valid user ID, or if scope["user"] is already populated)

        user = self.scope["user"]
        
        print("Trying to authenticate")
        try:
            tokenm = tokenreg.match(str(self.scope["query_string"]))
            if tokenm:
                # compatibility with rest framework
                auth_token = tokenm.group("token")
                print(auth_token)
                rf = RequestFactory()
                get_request = rf.get('/api/comments/')
                get_request._request = {}
                get_request.method = "GET"
                get_request.META["HTTP_AUTHORIZATION"] = "Bearer {}".format(auth_token)

                authenticators = [auth() for auth in api_settings.DEFAULT_AUTHENTICATION_CLASSES]
                for authenticator in authenticators:
                    user_auth_tuple = None
                    user_auth_tuple = await get_user(authenticator, get_request)
                    print(user_auth_tuple)
                    if user_auth_tuple is not None:
                        user, auth = user_auth_tuple
                        self.scope["auth"] = auth
                        self.scope["user"] = user
                        break

        except AttributeError as e:
            raise e
            logger.error("No Query String provided")
            pass


        inner = self.inner(self.scope)
        # Return the inner application directly and let it run everything else
        return await inner(receive, send)