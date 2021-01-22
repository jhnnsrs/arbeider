from datetime import timedelta, datetime
from django.contrib.auth import get_user_model
from guardian.utils import get_anonymous_user
from oauth2_provider.backends import OAuth2Backend
from rest_framework.request import Request
from rest_framework.settings import api_settings
from django.test import RequestFactory
from oauth2_provider.models import AccessToken, Application
import logging
from oauth2_provider.settings import oauth2_settings
from delt.constants.scopes import SCOPELIST
import re

logger = logging.getLogger(__name__)

try:
    application = Application.objects.get(name="Trontheim")
except:
    pass


tokenstring = re.compile(r'Bearer[\:]?\s*(?P<token>[\S]*)')


def authenticateFromRequest(request):
    
    authenticators = [auth() for auth in api_settings.DEFAULT_AUTHENTICATION_CLASSES]
    for authenticator in authenticators:
        user_auth_tuple = None
        user_auth_tuple = authenticator.authenticate(request) #TODO: No matter the request we can't detect auth for client credientals
        if user_auth_tuple is not None:
            logger.debug("Provided through OAuth2 Token")
            return user_auth_tuple
            
    
    return None, None



def authorize_by_token(token):
    auth = AccessToken.objects.get(token=token)
    user = auth.user

    return user, auth


def authenticateFromScopeAsContext(context):
    # This is from Session backend?
    user = context._scope["user"]
    auth = None
    return  user, auth



def authenticateFromAsgiRequest(request):


    authorization = request.META["HTTP_AUTHORIZATION"]
    m = tokenstring.match(authorization)
    if m:
        token = m.group("token")
        return authorize_by_token(token)

    return None, None 

SESSIONSCOPES = [k for k,v in SCOPELIST.items()]


class BouncerException(Exception):
    pass

class WrongAppTypeException(BouncerException):
    pass

class NoAnonymousAccess(BouncerException):
    pass


class BouncerContext(object):

    def __init__(self, request: Request = None, info= None, token=None):

        self.accessibles = []
        self.app_type = None
        self._user = None
        self._auth = None

        if request is not None:
            logger.info("Context Provided by Request Framework")
            self._user = request.user
            self._auth = request.auth

        
        if info is not None:
            logger.info("Context Provided by GraphQL Framework")
            context = info.context

            if hasattr(context, "_scope"): 
                self._user, self._auth = authenticateFromScopeAsContext(context)
            else:
                self._user, self._auth = authenticateFromAsgiRequest(context)
            

        if token is not None:
            logger.info("Context Provided by Token Framework")
            self._user, self._auth = authorize_by_token(token)



        if self._user : self.accessibles.append("user")
        if self._auth : self.accessibles.append("auth")
        
        if self._auth and self._user: self.app_type = "oauth"
        if self._auth and not self._user: self.app_type = "m2m"
        if not self._auth and self._user: self.app_type = "session"


        if not self._auth and not self._user:
            logger.warn("We are dealing with the M2M Error here or no Authentication") 
            self.app_type = "m2m" #TODO:This is correctly incorrect until we find a way to access the correct app
        

    def scopes(self, default= None):
        if "auth" not in self.accessibles:
            if default:
                return default
            else:
                raise Exception("No default scopes provided and client not authorized with scopes!")
        else:
            self._scopes = self._auth.scopes
        return self._scopes


    def can(self, scope, default=[]):
        try:
            if scope in self.scopes(default=default): return True 
        except Exception as e:
            if self.app_type == "m2m":
               return True
            else:
                raise e

        return False

    @property
    def app(self):
        return self.app_type

    @property
    def anonymous(self):
        return len(self.accessibles) < 1

    @property
    def accessible(self):
        return self.accessibles

    @property
    def user(self):
        if "user" not in self.accessibles:
            return get_anonymous_user()
        else:
            return self._user


    @property
    def token(self):
        # TODO: HORROUNDOUS
        if "auth" not in self.accessibles:
            logger.error("The App accessing this does not provide the right app type for TOKEN. Returnin Empty")
            return ""
        else:
            return self._auth




def bounce(apps = ["m2m","session","oauth"], accessible = ["user","app"], anonymous=False):

    def real_decorator(func):

        def bounced(cls, context: BouncerContext, *args, **kwargs):
            print(context)
            if context.app not in apps and len(apps) != 0:
                raise WrongAppTypeException(f"The client Authentication Type is not part of accessible App Type. {context.app} vs {apps}'")
            if accessible not in context.accessible and len(accessible) != 0:
                raise WrongAppTypeException(f'The client Authentication Type does not provide access to this Endpoint. {accessible} vs {context.accessible}')
            if anonymous:
                if context.anonymous: 
                    raise NoAnonymousAccess("Anonymous users or apps are not allowed on this Endpoint")
            return func(cls, context, *args, **kwargs)
        
        return bounced

    return real_decorator






