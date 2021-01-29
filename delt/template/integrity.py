import hashlib
from django.conf import settings
from delt.models import Node
import json

def template_identifier(node: Node, params=dict, withsecret= settings.SECRET_KEY):
    """This function generate 10 character long hash of the package and interface name"""
    hash = hashlib.sha1()
    salt = node.identifier + json.dumps(params)
    hash.update(salt.encode('utf-8'))
    return  hash.hexdigest()