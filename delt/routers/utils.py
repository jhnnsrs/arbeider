import hashlib
import inspect
from django.conf import settings

def route_identifier(package, interface, backend, withsecret= settings.SECRET_KEY):
    """This function generate 10 character long hash of the package and interface name"""
    hash = hashlib.sha1()
    salt = package + interface + backend + withsecret
    hash.update(salt.encode('utf-8'))
    return  hash.hexdigest()
