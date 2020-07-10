from django.contrib.auth import get_user_model
from guardian.utils import get_anonymous_user
from rest_framework.request import Request
from rest_framework.settings import api_settings
from django.test import RequestFactory
import logging

logger = logging.getLogger(__name__)


class BouncerContext(object):

    def __init__(self, request: Request = None, info= None, token=None, **kwargs):

        self._authorized = None
        self._scopes = None
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