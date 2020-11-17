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

    def __init__(self, app):
        # Store the ASGI application we were passed
        self.app = app

    async def __call__(self, scope, receive, send):

        # Close old database connections to prevent usage of timed out connections

        # Look up user from query string (you should also do things like
        # check it's a valid user ID, or if scope["user"] is already populated)

        user = scope["user"]
        
        print("Trying to authenticate")
        try:
            tokenm = tokenreg.match(str(scope["query_string"]))
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
                        scope["auth"] = auth
                        scope["user"] = user
                        break

        except AttributeError as e:
            raise e
            logger.error("No Query String provided")
            pass


        return await self.app(scope, receive, send)

