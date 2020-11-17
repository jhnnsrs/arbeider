from datetime import timedelta, datetime
from django.contrib.auth import get_user_model
from guardian.utils import get_anonymous_user
from rest_framework.request import Request
from rest_framework.settings import api_settings
from django.test import RequestFactory
from oauth2_provider.models import AccessToken, Application
import logging
from oauth2_provider.settings import oauth2_settings
from delt.constants.scopes import SCOPELIST

logger = logging.getLogger(__name__)

try:
    application = Application.objects.get(name="Trontheim")
except:
    pass




def authenticateFromRequest(request):
    
    authenticators = [auth() for auth in api_settings.DEFAULT_AUTHENTICATION_CLASSES]
    for authenticator in authenticators:
        user_auth_tuple = None
        user_auth_tuple = authenticator.authenticate(request)
        if user_auth_tuple is not None:
            logger.debug("Provided through OAuth2 Token")
            return user_auth_tuple
            
    
    return get_anonymous_user(), None


SESSIONSCOPES = [k for k,v in SCOPELIST.items()]

class BouncerContext(object):

    def __init__(self, request: Request = None, info= None, token=None, **kwargs):

        self._authorized = None
        self._scopes = None
        self._token = None
        if request is not None:
            logger.info("Context Provided by REST Framework")
            self._user = request.user
            self._auth = request.auth
            self._token = self._auth

        if info is not None:
            logger.info("Context Provided by GraphQL Framework")
            context = info.context
            try:
                self._user, self._auth = authenticateFromRequest(info.context)
                self._scopes = self._auth.scopes
                self._token = self._auth
            except:
                logger.info("Couldnt Authenticate with OAUTH, trying Session")
                try:
                    # This path means we are dealing with a session object
                    self._user = context._scope["user"]
                    self._auth = None
                    self._scopes = SESSIONSCOPES
                    self._token = "NONNONNONE"
                except Exception as e:
                    self._user = get_anonymous_user()
                    self._auth = None
                    self._scopes = []
                    self._token = "NONNONNONE"
                    logger.info("Failed completely here", e)

            #TODO: Impelement oauth thingy dingy

        if token is not None:
            logger.info("Context Provided by Token Framework")
            #TODO: Very very hacky
            # compatibility with rest framework
            self._token = token


            rf = RequestFactory()
            get_request = rf.get('/api/comments/')
            get_request._request = {}
            get_request.method = "GET"
            get_request.META["HTTP_AUTHORIZATION"] = "Bearer {}".format(token)

            self._user, self._auth = authenticateFromRequest(get_request)


        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)


    @property
    def scopes(self):
        if self._scopes is None:
            if self._auth is not None:
                self._scopes = self._auth.scopes
            else:
                self._scopes = []
        print(self._scopes)
        return self._scopes


    def can(self, scope):
        if scope in self.scopes: return True 



        return False

    @property
    def user(self):
        try:
            if self._user.id is None:
                self._user = get_anonymous_user()
            logger.debug(f"User is {self._user}")
            return self._user
        except:
            logger.error("Please fix this properly")
            return get_anonymous_user()


    @property
    def token(self):
        # TODO: HORROUNDOUS
        if self._token is None:
            try:
                self._token = AccessToken.objects.filter(user = self.user).first()
            except AccessToken.DoesNotExist as e:
                self._token = None
                logger.info("Creating new Access Token for this")

            if self._token is None: #Either we were login in anonymously or no token exists yet for this sort of applicatoin
                max_caching_time = datetime.now() + timedelta(
                    seconds=oauth2_settings.RESOURCE_SERVER_TOKEN_CACHING_SECONDS
                )
                self._token =  AccessToken.objects.create(user= self.user, application= application, expires= max_caching_time)
        return self._token