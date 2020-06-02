from rest_framework.request import Request
from guardian.shortcuts import get_perms
import logging

logger = logging.getLogger(__name__)

def is_authorized(permission, requiredscopes, user= None, instance =None, scopes=None, allow_no_scope=True):
    if user is not None:
        app_authorization = True
        grant_scope = "SESSION"
        if requiredscopes is not None:
            for scope in requiredscopes:
                if scopes is None and allow_no_scope:
                    break
                if scope in scopes:
                    app_authorization = True
                    grant_scope = scope
                    break
                else: 
                    app_authorization = False

        if app_authorization:
            if user is not None:
                if user.is_superuser:
                    logger.info(f"Authorized because of Super User Status and {grant_scope}-Scope")
                    return True
                if permission in get_perms(user, instance):
                    logger.info(f"Authorized because of Object Permission {permission} and {grant_scope}-Scope")
                    return True
                else:
                    return False


class Context(object):


    def __init__(self, request: Request = None, info= None, **kwargs):
        self._authorized = None
        self._scopes = None
        if request is not None:
            self._user = request.user
            self._auth = request.auth
        if info is not None:
            self._user = info.context._scope["user"]
            self._auth = None
            #TODO: Impelement oauth thingy dingy


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
        if self._user is None:
            self._user = None
        return self._user

    def is_authorized(self, permission, scopes=None, instance=None):
        return is_authorized(permission, scopes, user=self.user, instance=instance, scopes=self.scopes)

