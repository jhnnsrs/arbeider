from datetime import timedelta, datetime
from django.contrib.auth import get_user_model
from guardian.utils import get_anonymous_user
from rest_framework.request import Request
from rest_framework.settings import api_settings
from django.test import RequestFactory
from oauth2_provider.models import AccessToken, Application
import logging
from oauth2_provider.settings import oauth2_settings


logger = logging.getLogger(__name__)

try:
    application = Application.objects.get(name="Trontheim")
except:
    pass

class BouncerContext(object):

    def __init__(self, request: Request = None, info= None, token=None, **kwargs):

        self._authorized = None
        self._scopes = None
        self._token = None
        if request is not None:
            
            logger.info("Provided through preauthenticated Request")
            self._user = request.user
            self._auth = request.auth
        if info is not None:
            
            try:
                self._user = info.context._scope["user"]
                logger.info("Provided through preauthenticated Context _scope")
            except:
                self._user = info.context.user
                logger.info("Provided through preauthenticated Context")
            self._auth = None
            #TODO: Impelement oauth thingy dingy
        if token is not None:
            #TODO: Very very hacky
            # compatibility with rest framework
            self._token = token


            rf = RequestFactory()
            get_request = rf.get('/api/comments/')
            get_request._request = {}
            get_request.method = "GET"
            get_request.META["HTTP_AUTHORIZATION"] = "Bearer {}".format(token)

            authenticators = [auth() for auth in api_settings.DEFAULT_AUTHENTICATION_CLASSES]
            for authenticator in authenticators:
                user_auth_tuple = None
                user_auth_tuple = authenticator.authenticate(get_request)
                if user_auth_tuple is not None:
                    logger.info("Provided through OAuth2 Token")
                    self._user, self._auth = user_auth_tuple
                    
                else:
                    self._user = get_anonymous_user()


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
        return self._scopes     

    @property
    def user(self):
        if self._user.id is None:
            self._user = get_anonymous_user()
        logger.info(f"User is {self._user}")
        return self._user


    @property
    def token(self):
        # TODO: HORROUNDOUS
        if self._token is None:
            try:
                self._token = AccessToken.objects.filter(user = self.user, application = application).first()
            except AccessToken.DoesNotExist as e:
                logger.info("Creating new Access Token for this")
                max_caching_time = datetime.now() + timedelta(
                    seconds=oauth2_settings.RESOURCE_SERVER_TOKEN_CACHING_SECONDS
                )
                self._token =  AccessToken.objects.create(user= self.user, application= application, expires= max_caching_time)
        return self._token