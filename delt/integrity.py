
import hashlib
from django.conf import settings


def node_identifier(package, interface, withsecret= settings.SECRET_KEY):
    """This function generate 10 character long hash of the package and interface name"""
    
    
    assert(package), "Integrity Error:  Define Package"
    assert(interface), "Integrity Error: Define Interface"

    hash = hashlib.sha1()
    salt = package + interface + withsecret
    hash.update(salt.encode('utf-8'))
    return  hash.hexdigest()