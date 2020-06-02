from rest_framework.request import Request
from django.contrib.auth import get_user_model

class BouncerContext(object):

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
        if self._user.id is None:
            print("NO USER")
            self._user = get_user_model().objects.get(id=1)
        print("USER", self._user)
        return self._user